
// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
frappe.query_reports["Vehicle Insurance"] = {
	"filters": [
		// {
		// 	"fieldname": "filter_based_on",
		// 	"label": __("Filter Based On"),
		// 	"fieldtype": "Select",
		// 	"options": ["Fiscal Year", "Date Range"],
		// 	"default": ["Fiscal Year"],
		// 	"reqd": 1
		// },
		// {
		// 	"fieldname": "fiscal_year",
		// 	"label": __("Fiscal Year"),
		// 	"fieldtype": "Link",
		// 	"options": "Fiscal Year",
		// 	"default": frappe.defaults.get_user_default("fiscal_year"),
		// 	"depends_on": "eval: doc.filter_based_on == 'Fiscal Year'",
		// 	"reqd": 1
		// },
		// {
		// 	"fieldname": "from_date",
		// 	"label": __("From Date"),
		// 	"fieldtype": "Date",
		// 	// "reqd": 1,
		// 	// "depends_on": "eval: doc.filter_based_on == 'Date Range'",

		// 	"default": frappe.datetime.add_months(frappe.datetime.nowdate(), -12)
		// },
		{
			"fieldname": "to_date",
			"label": __("Expiry Date"),
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
			"fieldname": "insurance_company",
			"label": __("Insurance Company"),
			"fieldtype": "Link",
			"options": "Insurance Company"
		},
		{
			"fieldname": "ownership",
			"label": __("Ownership"),
			"fieldtype": "Link",
			"options": "Vehicle Ownership"

		}
	]
};
