# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe

# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns(filters)
	data = get_data(filters)
	# chart = get_chart_data(data)

	return columns, data, None
	# , chart

def get_columns(filters=None):
	columns = [
			{
				"label": _("Vehicle No"),
				"fieldname": "name",
				"fieldtype": "Link",
				"options": "Vehicle",
				"width": 125
			},
			{
				"label": _("Model"),
				"fieldname": "model",
				"fieldtype": "Data",
				"width": 175
			},
			{
				"label": _("Vehicle Holder"),
				"fieldname": "employee_name",
				"fieldtype": "Data",
				"width": 120
			},
			{
				"label": _("Driver"),
				"fieldname": "full_name",
				"fieldtype": "Data",
				# "options": "Driver",
				"width": 120
			},
			
			{
				"label": _("License Number"),
				"fieldname": "license_number",
				"fieldtype": "Data",
				"width": 120
			},
			{
				"label": _("License Expiry"),
				"fieldname": "expiry_date",
				"fieldtype": "Data",
				"width": 120
			}
	]

	return columns
# def get_data(filters = None):
# 	conditions = get_filter_conditions(filters)
# 	data = frappe.db.sql("""
# 			SELECT i.name, i.item_name, i.item_code, ib.end_of_life from `tabSerial No` as i join `tabItem` ib on ib.item_code = i.item_code where i.item_code = %s""" % (conditions),  as_dict=1)
# 	return data

@frappe.whitelist()
def get_data(filters = None):
	conditions = get_filter_conditions(filters)
	data = frappe.db.sql("""
			select v.name, v.model, v.employee_name ,d.employee , d.full_name ,d.license_number ,d.expiry_date from `tabDriver` d, `tabFleet Vehicle` v Where v.driver = d.name %s""" % (conditions),  as_dict=1)
	# print('data ', data)
	return data


def get_filter_conditions(filters):
	conditions = ""

	# if filters.get('from_date') and filters.get('to_date'):
	# 	conditions += " and expiry_date BETWEEN '%s' and '%s'" % (filters.get("from_date"), filters.get("to_date"))
	
	if filters.get("d.name"):
		conditions += " and d.name = '%s' " % (filters.get("d.name"))
	if filters.get("v.name"):
		conditions += " and v.name = '%s' " % (filters.get("v.name"))

	# if filters.get("warehouse"):
	# 	conditions += " and warehouse = '%s' " % (filters.get("warehouse"))
	
	# if filters.get("batch_no"):
	# 	conditions += " and batch_no = '%s' " % (filters.get("batch_no"))

	# if filters.get("serial_no"):
	# 	conditions += " and serial_no = '%s' " % (filters.get("serial_no"))

	# if filters.get("item_code"):
	# 	conditions += " and item_code = '%s' " % (filters.get("item_code"))
	
	# if filters.get("status"):
	# 	conditions += " and status = '%s' " % (filters.get("status"))

	# if filters.get("area"):
	# 	conditions += " and area  = '%s' " % (filters.get("area"))

	return conditions
