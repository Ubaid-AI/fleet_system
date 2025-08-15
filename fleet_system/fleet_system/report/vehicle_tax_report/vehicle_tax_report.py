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
				"fieldname": "license_plate",
				"fieldtype": "Link",
				"options": "Vehicle",
				"width": 125
			},
			{
				"label": _("Engine No"),
				"fieldname": "engine_no",
				"fieldtype": "Data",
				"width": 175
			},
			{
				"label": _("Chassis No"),
				"fieldname": "chassis_no",
				"fieldtype": "Data",
				"width": 120
			},
			{
				"label": _("Branch Name"),
				"fieldname": "branch_name",
				"fieldtype": "Data",
				# "options": "Driver",
				"width": 120
			},
			{
				"label": _("From"),
				"fieldname": "tax_paid_from",
				"fieldtype": "Date",
				"width": 120
			},
			{
				"label": _("Upto"),
				"fieldname": "upto",
				"fieldtype": "Date",
				"width": 120
			},
			
			{
				"label": _("Challan No"),
				"fieldname": "challan_no",
				"fieldtype": "Data",
				"width": 120
			},
			{
				"label": _("Amount"),
				"fieldname": "cash_amount",
				"fieldtype": "Data",
				"width": 120
			},
			{
				"label": _("Last Challan No"),
				"fieldname": "last_challan_no",
				"fieldtype": "Data",
				"width": 120
			},
						{
				"label": _("Last Amount Paid"),
				"fieldname": "last_amount_paid",
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
	if filters.from_date > filters.to_date:
		frappe.throw(_("From Date cannot be greater than To Date"))
	conditions = get_filter_conditions(filters)
	start_date, end_date = filters.from_date, filters.to_date
	values = {
		'start_date': start_date,
		'end_date': end_date
	}

	data = frappe.db.sql("""
		SELECT license_plate, engine_no , chassis_no ,branch_name, tax_paid_from, upto, challan_no, cash_amount, last_challan_no, last_amount_paid 
		from `tabVehicle Tax` 
		WHERE
		 upto between %(start_date)s and %(end_date)s
		and docstatus = 0 {0}""".format(conditions), values,  as_dict=1)
	not_in_tax = frappe.db.sql(""" 
			SELECT license_plate, employee_name, ownership  from `tabFleet Vehicle` tv
			Where tv.vehical_type = 'Car' 
			and tv.name  Not in (SELECT license_plate from `tabVehicle Tax`)
		""", as_dict=1)
	not_paid = frappe.db.sql(""" 
			SELECT tv.license_plate, tv.employee_name, tv.ownership, tt.upto from `tabFleet Vehicle` tv, `tabVehicle Tax` tt
			WHERE tt.upto< SYSDATE() and tv.license_plate not in (SELECT license_plate from `tabVehicle Tax` WHERE upto > SYSDATE() )
			and tv.license_plate  = tt.license_plate 
		""", as_dict=1)
	if data:
		data[-1]['not_in_tax'] = not_in_tax
		data[-1]['not_paid'] = not_paid
	# with open('/home/frappe/frappe-bench/apps/erpnext/erpnext/fleet_ms/report/vehicle_tax_report/tttt.txt', 'w+') as f:
	# 	f.writelines(str(data[-1]))
	# print('data ', data)
	return data


def get_filter_conditions(filters):
	conditions = ""
	
	# if filters.get('from_date') and filters.get('to_date'):
	# 	conditions += " and expiry_date BETWEEN '%s' and '%s'" % (filters.get("from_date"), filters.get("to_date"))
	
	if filters.get("license_plate"):
		conditions += " and license_plate = '%s' " % (filters.get("license_plate"))
	if filters.get("challan_no"):
		conditions += " and challan_no = '%s' " % (filters.get("challan_no"))

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
            # {% var not_paid = []; %}
            # {% var not_in_tax =[]; %}
            # {% not_paid = data[data.length-2].not_paid  || [] %}
            # {% not_in_tax = data[data.length-2].not_in_tax || [] %}

# // Online Javascript Editor for free
# // Write, Edit and Run your Javascript code using JS Online Compiler
# const vehicles = [
#   { license_plate: 'ABC123', employee_name: 'John', ownership: 'owned' },
#   { license_plate: 'DEF456', employee_name: 'Jane', ownership: 'leased' },
#   { license_plate: 'JKL012', employee_name: 'Bob', ownership: 'owned' },
# ];

# const vehicleTaxData = [
#   { license_plate: 'ABC123', next_tax_date: '2023-01-01' },
#   { license_plate: 'DEF456', next_tax_date: '2023-02-01' },

# ];
# const notInTax = vehicles.filter(vehicle => {
#   return !vehicleTaxData.find(data => data.license_plate == vehicle.license_plate);
# }).map(vehicle => {
#   return {
#     license_plate: vehicle.license_plate,
#     employee_name: vehicle.employee_name,
#     ownership: vehicle.ownership,
#   };
# });

# console.log('Not in tax:', notInTax);

# // Expired tax array
# const expiredTax = vehicleTaxData.filter(data => {
#   const nextTaxDate = new Date(data.next_tax_date);
#   const currentDate = new Date();
#   return nextTaxDate < currentDate;
# }).map(data => {
#   console.log(data)
#   return {
      
#     license_plate: data.license_plate,
#     employee_name: vehicles.find(vehicle => vehicle.license_plate == data.license_plate).employee_name,
#     ownership: vehicles.find(vehicle => vehicle.license_plate === data.license_plate).ownership,
#     expiry_date: data.next_tax_date,
#   };
# }).filter((value, index, self) => {
#   // Remove duplicates
#   return index === self.findIndex(obj => obj.license_plate === value.license_plate);
# });
# console.log(expiredTax)


# {%
# var greater = frappe.db.get_list('Vehicle Tax', {
# 	filters:{
# 		'upto': ['>=', frappe.datetime.nowdate()],
# 	},
# 	fields: ['license_plate', 'upto'],
# 	limit: 500,
#     order_by: 'license_plate',
# 	}).then(greater => {
# 		return greater
# 	});
# %}
# {%
# var less = frappe.db.get_list('Vehicle Tax', {
# 	filters:{
# 		'upto': ['<', frappe.datetime.nowdate()],
# 	},
# 	fields: ['license_plate', 'upto'],
# 	limit: 500,
#     order_by: 'license_plate',
# 	}).then(less => {
# 		return less
# 	});
# %}


#   var gt = await greater;
#   var lt = await less;
#   for (const obj of lt) {

#   if (!gt.some(o => o.license_plate === obj.license_plate)) {
#     not_in.push(obj);
#   }
# }
# for (const v of vh){
#     if (not_in.some(o => o.license_plate === v.license_plate)) {
#         not_paid.push(v);
#       }
# }
# {% not_paid = data[data.length-2].not_paid  || [] %}
#             {% not_in_tax = data[data.length-2].not_in_tax || [] %}