"""
CNPJ and CPF validation script
Implementes in ERP Odoo by Q.Factor IT (2019)
"""
def onchange_validate_registry(self):
#import re
#from odoo.exceptions import UserError
#from odoo import    
    if self.company_registry:
        self.company_registry = re.sub('[^0-9]', '', self.company_registry)
        
        if len(self.company_registry) == 11 or len(self.company_registry) == 14:
            number_check_digits = 1
            original_check_digits = self.company_registry[-2:]
            base_number = self.company_registry[:-2]
            registry_number_list = []
            
            if len(self.company_registry) == 11:
                registry_sequence = list(range(2, 12))
            else:
                registry_sequence = list(range(2, 10))
            
            for numbers in base_number:
                registry_number_list.append(int(numbers))
            
            while number_check_digits <= 2:
                new_check_digits = fields_custom.check_digits(self, registry_number_list, registry_sequence)
                
                if new_check_digits >= 10:
                    new_check_digits = 0
                registry_number_list.append(new_check_digits)
                number_check_digits += 1
            
            new_check_digits = f"{registry_number_list[-2]}{registry_number_list[-1]}"
            
            if original_check_digits == new_check_digits:
                self.company_registry = fields_custom.format_value(self, self.company_registry)
            else:
                raise UserError(_("Invalid Registry Number"))
        else:
            raise UserError(_("Invalid Registry Number."))

def onchange_validate_person_identify(self, person_identify):
#import re
#from odoo.exceptions import UserError
#from odoo import
	if person_identify:
		person_identify = re.sub('[^0-9]', '', person_identify)

		if len(person_identify) == 9:
			number_check_digits = 1
			original_check_digits = person_identify[-2:]
			base_number = person_identify[:-2]
			person_identify_sequence = list(range(2, 10))
			person_identify_list = []

			for numbers in base_number:
				company_registry_list.append(int(numbers))

			while number_check_digits == 1:
				new_check_digits = check_digits(person_identify_list, person_identify_sequence)

				if new_check_digits == 11:
					new_check_digits = 0
				elif new_check_digits == 10:
					new_check_digits = "X"

				person_identify_list.append(new_check_digits)
				number_check_digits += 1

			new_check_digits = person_identify_list[-2:]
			new_check_digits = "%s%s" % (new_check_digits[0], new_check_digits[1])

			if original_check_digits == new_check_digits:
				person_identify = format_value(person_identify)
			else:
				raise UserError(_("Invalid Person Identify"))
		else:
			raise UserError(_("Invalid Person Identify"))

def format_value(self, vals):
    
    if len(vals) == 14:
        return "%s.%s.%s/%s-%s" % (vals[0:2], vals[2:5], vals[5:8], vals[8:12], vals[12:14])
    elif len(vals) == 11:
        return "%s.%s.%s-%s" % (vals[0:3], vals[3:6], vals[6:9], vals[9:11])
    else:
    	return "%s.%s.%s-%s" % (vals[0:2], vals[3:6], vals[6:9], vals[9])

def check_digits(self, registry_number_list, company_registry_sequence):
        id = 0
        result = 0
        registry_number_list = registry_number_list[::-1]
        
        for seq in registry_number_list:
            seq *= company_registry_sequence[id]
            result += seq
            
            if company_registry_sequence[id] == company_registry_sequence[-1]:
                id = 0
            else:
                id += 1
        
        result %= 11
        new_digit = 11 - result
        return new_digit

