# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import json

from frappe import _
from frappe.utils import flt



def execute(filters=None):
	filters = frappe._dict(filters or {})

	columns = get_columns()
	data = get_vehicle_history(filters)

	return columns, data

def get_vehicle_history(filters):
	conditions, values = get_conditions(filters)
	data = frappe.db.sql("""
		SELECT modified , modified_by , ref_doctype , docname , data from tabVersion
		where modified BETWEEN %(start_date)s and %(end_date)s
		and ref_doctype = 'Vehicle' {0}
		ORDER BY modified""".format(conditions), values, as_dict=1)
	new_data = []
	for idx, row in enumerate(data):
		changed_list = json.loads(row['data']).get('changed') 
		# f.writelines(str(json.loads(row['data'])))
		if changed_list:
			if 'sum_insured' in changed_list[0] or 'market_value' in changed_list[0]:
				data[idx]['modified_field'] = changed_list[0][0].replace('_', ' ').title()
				data[idx]['previous_value'] = changed_list[0][1]
				data[idx]['new_value'] = changed_list[0][2]
				new_data.append(data[idx])
	del data
	return new_data


def get_conditions(filters):
	conditions = ''

	start_date, end_date = filters.from_date, filters.to_date
	values = {
		'start_date': start_date,
		'end_date': end_date
	}


	if filters.license_plate:
		conditions += ' and docname = %(vehicle)s'
		values['vehicle'] = filters.license_plate

	if filters.modified_by:
		conditions += ' and modified_by = %(modified_by)s'
		values['modified_by'] = filters.modified_by
		
	return conditions, values

def get_columns():
	return [
		{
			'fieldname': 'modified',
			'fieldtype': 'Date',
			'label': _('Modified Date'),
			'width': 225
		},
		{
			'fieldname': 'modified_by',
			'fieldtype': 'Link',
			'label': _('Modified By'),
			'options': 'User',
			'width': 210
		},
		# {
		# 	'fieldname': 'ref_doctype',
		# 	'fieldtype': 'Data',
		# 	'label': _('Doctype'),
		# 	'width': 70
		# },
		{
			'fieldname': 'docname',
			'fieldtype': 'Link',
			'label': _('License Plate'),
			'options': 'Vehicle',
			'width': 80
		},
		{
			'fieldname': 'modified_field',
			'fieldtype': 'Data',
			'label': _('Modified Field'),
			'width': 110
		},
		{
			'fieldname': 'previous_value',
			'fieldtype': 'Data',
			'label': _('Previous Value'),
			'width': 100
		},
		{
			'fieldname': 'new_value',
			'fieldtype': 'Data',
			'label': _('New Value'),
			'width': 80
		},
	
	]
