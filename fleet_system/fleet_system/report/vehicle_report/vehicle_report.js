
// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
frappe.query_reports["Vehicle Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",

			"default": frappe.datetime.add_months(frappe.datetime.nowdate(), -12)
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			// "reqd": 1,
			// "depends_on": "eval: doc.filter_based_on == 'Date Range'",
			"default": frappe.datetime.add_months(frappe.datetime.nowdate(), +24),
			"description":"to expiry date"
		},
		{
			"fieldname": "license_plate",
			"label": __("Vehicle"),
			"fieldtype": "Link",
			"options": "Fleet Vehicle"
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
			"fieldname": "ownership",
			"label": __("Ownership"),
			"fieldtype": "Data"
		}
	]
};
