# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2010-2014 Elico Corp. All Rights Reserved.
#    Augustin Cisterne-Kaas <augustin.cisterne-kaas@elico-corp.com>
#    Eric Caudal <eric.caudal@elico-corp.com>

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
from openerp.tools.translate import _
from openerp.addons.connector.queue.job import job
from openerp.addons.connector.unit.synchronizer import ExportSynchronizer
from ..connector import get_environment
from openerp.addons.connector.exception import MappingError
from osv import osv

_logger = logging.getLogger(__name__)
"""

Exporters for ICOPS.

In addition to its export job, an exporter has to:

* check in ICOPS if the record has been updated more recently than the
  last sync date and if yes, delay an import
* call the ``bind`` method of the binder to update the last sync date

"""


class ICOPSBaseExporter(ExportSynchronizer):

    """ Base exporter for ICOPS """

    def __init__(self, environment):
        """
        :param environment: current environment (backend, session, ...)
        :type environment: :py:class:`connector.connector.Environment`
        """
        super(ICOPSBaseExporter, self).__init__(environment)
        self.binding_id = None
        self.icops_ids = {}

    def _get_openerp_data(self):
        """ Return the raw OpenERP data for ``self.binding_id`` """
        return self.session.browse(self.model._name, self.binding_id)

    def run(self, binding_id, *args, **kwargs):
        """ Run the synchronization

        :param binding_id: identifier of the binding record to export
        """
        self.binding_id = binding_id
        self.binding_record = self._get_openerp_data()

        self.icops_ids = self.binder.to_backend(self.binding_id)
        result = self._run(*args, **kwargs)
        self.binder.bind(self.icops_ids, self.binding_id)
        return result

    def _run(self):
        """ Flow of the synchronization, implemented in inherited classes"""
        raise NotImplementedError


class ICOPSExporter(ICOPSBaseExporter):

    _concepts = None
    """ A common flow for the exports to ICOPS """
    def __init__(self, environment):
        """
        :param environment: current environment (backend, session, ...)
        :type environment: :py:class:`connector.connector.Environment`
        """
        super(ICOPSExporter, self).__init__(environment)
        self.binding_record = None

    def _has_to_skip(self):
        """ Return True if the export can be skipped """
        return False

    def _routing(self, record, fields=None, backward=False):
            sess = self.session
            fields = fields or []
            icops = self.mapper._icops
            icops_id = None
            if backward:
                icops_id = sess.pool.get(
                    self.binding_record.icops_model).browse(
                    sess.cr, 1, self.binding_record.icops_id).openerp_id.id

            else:
                icops_id = self._get_icops_id(
                    icops.backend_to.id, icops.concept)
            if not icops_id:
                return
            if 'icops_delete' in fields:
                self._delete(icops_id)
            else:
                self._custom_routing(icops_id, record, fields)

    def _custom_routing(self, id, record, fields=None):
        self._write(id, record)

    def _run(self, fields=None):
        """ Flow of the synchronization, implemented in inherited classes"""
        assert self.binding_id
        assert self.binding_record

        if not self.icops_ids:
            fields = None  # should be created with all the fields

        if self._has_to_skip():
            return

        nb_records = 0
        icops_ids = {}

        #if self.binding_record.locked and 'backward' not in\
        #        self.session.context:
        #    self.session.context.update({'backward': True})
        #    for icops in self._get_backward_icops():
        #        backend = self._get_backend_with_permission(
        #            icops, backward=True)
        #        self._set_icops(icops, backend, backward=True)
        #        try:
        #            self._map_data(fields=fields)
        #        except MappingError:
        #            continue
        #        record = self.mapper.data
        #        if not record:
        #            continue
        #        self._validate_data(record)
        #        self._routing(record, fields, backward=True)

        for icops in self._get_icops():
            backend = self._get_backend_with_permission(icops)
            self._set_icops(icops, backend)
            try:
                self._map_data(fields=fields)
            except MappingError:
                continue
            if self.icops_ids:
                record = self.mapper.data
                if not record:
                    continue
                nb_records += 1
                self._validate_data(record)
                self._routing(record, fields)
            else:
                record = self.mapper.data_for_create
                if not record:
                    continue
                nb_records += 1
                self._validate_data(record)
                key = '%s_%s' % (icops.backend_to.id, icops.concept)
                icops_ids[key] = {
                    'id': self._create(record),
                    'model': self.backend_adapter._get_pool()._name
                }

        self.icops_ids = icops_ids

        if nb_records == 0:
            return _('Nothing to export.')
        return _('Record exported.')

    def _get_backend_with_permission(self, icops, backward=False):
        sess = self.session
        # don't know the ic_uid in case of reverse backend
        ic_uid = icops.backend_id.icops_uid.id if backward else icops.icops_uid.id
        backend = icops.backend_id.id if backward else icops.backend_to.id
        backend_pool = sess.pool.get('icops.backend')
        return backend_pool.browse(
            sess.cr, ic_uid, backend)

    def _get_icops(self):
        res = []
        # test
        sess = self.session
        user_pool = sess.pool.get('res.users')
        user = user_pool.browse(sess.cr, sess.uid, sess.uid)
        backend_pool = sess.pool.get('icops.backend')
        backend_ids = backend_pool.search(
            sess.cr, sess.uid, [('company_id', '=', user.company_id.id)])
        if not backend_ids:
            return res
        intercompany_pool = sess.pool.get('res.intercompany')
        intercompany_ids = intercompany_pool.search(
            sess.cr, sess.uid,
            [('backend_id', '=', backend_ids[0]),
             ('concept', 'in', self._concepts)])
        res = intercompany_pool.browse(sess.cr, sess.uid, intercompany_ids)
        return res

    def _get_backward_icops(self):
        assert self.binding_id
        assert self.binding_record
        res = []
        sess = self.session
        icops_obj = sess.pool.get(self.binding_record.icops_model).browse(
            sess.cr, 1, self.binding_record.icops_id)

        backend_pool = sess.pool.get('icops.backend')
        backend_ids = backend_pool.search(
            sess.cr, icops_obj.user_id.id,
            [('company_id', '=', icops_obj.company_id.id)])
        if not backend_ids:
            return res
        intercompany_pool = sess.pool.get('res.intercompany')
        # reverse concepts
        concepts = []
        for concept in self._concepts:
            temp_concept = list(concept.partition('2'))
            temp_concept.reverse()
            concepts.append(''.join(temp_concept))

        intercompany_ids = intercompany_pool.search(
            sess.cr, icops_obj.user_id.id,
            [('backend_id', '=', backend_ids[0]),
             ('concept', 'in', concepts)])
        res = intercompany_pool.browse(sess.cr, sess.uid, intercompany_ids)
        return res

    def _set_icops(self, icops, backend, backward=False):
        # backward
        self.mapper._backward = backward
        self.backend_adapter._backward = backward
        self.mapper._icops = icops
        self.backend_adapter._icops = icops
        self.mapper._backend_to = backend
        self.backend_adapter._backend_to = backend

    def _create(self, data):
        if not self.backend_adapter._icops.on_create:
            raise osv.except_osv('ICOPS Error', 'Can\'t create')
        return self.backend_adapter.create(data)

    def _write(self, id, data):
        context = self.session.context or {}
        if (not self.backend_adapter._icops.on_write and 'icops' not in context)\
                and 'backward' not in context:
            raise osv.except_osv('ICOPS Error', 'Can\'t write')
        self.backend_adapter.write(id, data)

    def _confirm(self, id):
        context = self.session.context or {}
        if (not self.backend_adapter._icops.on_confirm and 'icops' not in context)\
                and 'backward' not in context:
            raise osv.except_osv('ICOPS Error', 'Can\'t confirm')
        self.backend_adapter.confirm(id)

    def _cancel(self, id):
        context = self.session.context or {}
        if (not self.backend_adapter._icops.on_cancel and 'icops' not in context)\
                and 'backward' not in context:
            raise osv.except_osv('ICOPS Error', 'Can\'t cancel')
        self.backend_adapter.cancel(id)

    def _delete(self, id):
        context = self.session.context or {}
        if not self.backend_adapter._icops.on_unlink:
            raise osv.except_osv('ICOPS Error', 'Can\'t delete')
        self.backend_adapter.delete(id)

    def _map_data(self, fields=None):
        """ Convert the external record to OpenERP """
        self.mapper.convert(self.binding_record, fields=fields)

    def _validate_data(self, data):
        """ Check if the values to export are correct

        Pro-actively check before the ``Model.create`` or
        ``Model.update`` if some fields are missing

        Raise `InvalidDataError`
        """
        return

    def _get_icops_id(self, backend_id, concept):
        key = '%s_%s' % (backend_id, concept)
        try:
            return self.icops_ids[key]['id']
        except:
            return None


@job
def export_record(session, model_name, binding_id, fields=None):
    """ Export a record on ICOPS """
    record = session.browse(model_name, binding_id)
    env = get_environment(session, model_name, record.backend_id.id)
    exporter = env.get_connector_unit(ICOPSExporter)
    return exporter.run(binding_id, fields=fields)
