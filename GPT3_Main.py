

# dict= {'Name': 'Alexander Ortega', 
#        'Company': 'Bimbo',
#        'Position': 'Data Scientist',
#        'Time_in_position': '3 mos',
#        'Location': 'Bogotá',
#        'Education': 'MIT',
#        'Option': 3
#        }

from GPT3_Functions import multi_icebreack_message


def ice(dict):
    salida = multi_icebreack_message(dict)
    return salida

