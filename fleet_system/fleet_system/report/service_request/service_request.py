# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns()
	data = get_data(filters)
	# chart = get_chart_data(data, filters)

	return columns, data, None
	# , chart

def get_columns():
	return [
		{
			'fieldname': 'license_plate',
			'fieldtype': 'Link',
			'label': _('Vehicle'),
			'options': 'Vehicle'
		},
		{
			'fieldname': 'days_left',
			'fieldtype': 'Int',
			'label': 'Days Left'
		},
		{
			'fieldname': 'initiated_date',
			'fieldtype': 'Date',
			'label': _('Initiated Date')
		},
		{
			'fieldname': 'due_date',
			'fieldtype': 'Date',
			'label': _('Due Date')
		},
		{
			'fieldname':'allowed_amount',
			'fieldtype':'Currency',
			'label':'Recommended Amount'
		},
		{
			'fieldname':'service_type',
			'fieldtype':'Data',
			'label':'Item'
		},
		

	]


def get_data(filters):

	conditions, values = get_conditions(filters)

	data = frappe.db.sql("""
		SELECT tsr.license_plate, tsr.name,  DATEDIFF(tsr.due_date, CURDATE()) AS days_left, service_type, tsr.initiated_date, tsr.due_date, tsr.allowed_amount
		FROM `tabService Request` tsr WHERE tsr.status='Recommended' {0}""".format(conditions), values, as_dict=1)
	
	return data


def get_conditions(filters):
	conditions = ''
	values = {}

	if filters.license_plate:
		conditions += ' and tsr.license_plate = %(license_plate)s'
		values['license_plate'] = filters.license_plate

	return conditions, values



@frappe.whitelist()
def update_approved_status(status, name):
    doc = frappe.get_doc("Service Request", name)
    doc.status = status
    doc.save()
    frappe.msgprint("Record updated successfully!")