

// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
frappe.require("assets/erpnext/js/vehicle_expenses_formatter.js",  function() {
	frappe.query_reports["Vehicle Last Expenses Report"] = {
		"filters": [
			{
				"fieldname": "from_date",
				"label": __("From Date"),
				"fieldtype": "Date",
				"reqd": 1,
				// "depends_on": "eval: doc.filter_based_on == 'Date Range'",
				"default": frappe.datetime.add_months(frappe.datetime.nowdate(), -24)
			},
			{
				"fieldname": "to_date",
				"label": __("To Date"),
				"fieldtype": "Date",
				"reqd": 1,
				// "depends_on": "eval: doc.filter_based_on == 'Date Range'",
				"default": frappe.datetime.nowdate()
			},
			{
				"fieldname": "vehicle",
				"label": __("Vehicle"),
				"fieldtype": "Link",
				"options": "Fleet Vehicle"
			},
			{
				"fieldname": "employee",
				"label": __("Employee"),
				"fieldtype": "Link",
				"options": "Employee"
			}
		],
		"formatter": erpnext.vehicle_expenses_report.formatter,
			"tree": true,
			"name_field": "vehicles",
			"parent_field": "vehicle_parent",
			"initial_depth": 3
		,
	
	};
});
	