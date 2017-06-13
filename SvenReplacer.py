class SvenReplacer:

    def Patchnote_replace(text):
        string = text
        string = string.replace('_', ' ')
        string = string.replace('Attribute', ' ')
        string = string.replace('special', ' ')
        string = string.replace('Ability10', 'TalentTree Level 10')
        string = string.replace('Ability11', 'TalentTree Level 10')
        string = string.replace('Ability12', 'TalentTree Level 15')
        string = string.replace('Ability13', 'TalentTree Level 15')
        string = string.replace('Ability14', 'TalentTree Level 20')
        string = string.replace('Ability15', 'TalentTree Level 20')
        string = string.replace('Ability16', 'TalentTree Level 25')
        string = string.replace('Ability17', 'TalentTree Level 25')
        string = string.replace('Status', '')
        return string
    
#testkrams
    
# text = '''Changes For Bloodseeker:
#     AttackDamageMin was change from 29 to 33
#     AttackDamageMax was change from 35 to 39
# Changes For Crystal Maiden:
#     MovementSpeed was change from 280 to 275
# Changes For Zeus:
#     MovementSpeed was change from 295 to 300
# Changes For Venomancer:
#     AttributeAgilityGain was change from 2.600000 to 2.800000
# Changes For Viper:
#     Ability12 was change from special_bonus_strength_10 to special_bonus_strength_15
# Changes For Shadow Demon:
#     Ability10 was change from special_bonus_strength_6 to special_bonus_strength_10
#     Ability11 was change from special_bonus_movement_speed_10 to special_bonus_movement_speed_20
#     Ability13 was change from special_bonus_spell_amplify_6 to special_bonus_spell_amplify_8
#     Ability14 was change from special_bonus_magic_resistance_10 to special_bonus_magic_resistance_15
# Changes For Treant Protector:
#     MovementSpeed was change from 290 to 280
# Changes For Skywrath Mage:
#     Ability14 was change from special_bonus_movement_speed_20 to special_bonus_movement_speed_40
#     Ability15 was change from special_bonus_magic_resistance_15 to special_bonus_magic_resistance_20
# Changes For Ember Spirit:
#     Ability10 was change from special_bonus_spell_amplify_10 to special_bonus_spell_amplify_8
#     Ability11 was change from special_bonus_attack_damage_25 to special_bonus_attack_damage_30
# Changes For Monkey King:
#     Ability11 was change from special_bonus_armor_5 to special_bonus_evasion_10
#     StatusHealthRegen was change from 0.750000 to 1.50000'''
#
# ausgabe = SvenReplacer.Patchnote_replace(text)
# print(ausgabe)
