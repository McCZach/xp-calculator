import sys, os

def build_xp_table():
    xp_dict = {}

    try:
        filepath = 'data/xp.csv'
        if hasattr(sys, '_MEIPASS'):
            filepath = os.path.join(sys._MEIPASS, filepath)

        xp_file = open(filepath, 'r')
    except:
        print('ERROR - Could not open file.')
        return xp_dict
    else:
        line = xp_file.readline().rstrip()
        while line != '':
            xp = line.split(',')

            key = xp[0]
            xp_dict[key] = [int(item) for item in xp[1::]]

            line = xp_file.readline().rstrip()
    
    xp_file.close()
    return xp_dict

def get_default_input():
    num_monster = int(input('Enter the number of Monsters: '))
    hit_dice = int(input('Enter the amount of Hit Dice: '))
    hit_points = int(input('Enter the amount of Hit Points: '))

    special = input('Special Ability (Y/N)? ').lower()
    if special.isdigit():
        raise Exception
    exceptional = input('Exceptional Ability (Y/N)? ').lower()
    if exceptional.isdigit():
        raise Exception
    
    return num_monster, hit_dice, hit_points, special, exceptional

def get_default_xp(xp_dict: dict, num_monster: int, hit_dice: int, hit_points: int, special: str, exceptional: str):
    xp_amount = 0

    for key in xp_dict:
        if int(key) == hit_dice:
            xp_amount = xp_dict[key][0]
            xp_amount += (xp_dict[key][1] * hit_points)
            if special == 'y':
                xp_amount += xp_dict[key][2]
            if exceptional == 'y':
                xp_amount += xp_dict[key][3]

            xp_amount *= num_monster
            break
    
    return xp_amount

def get_custom_input():
    num_monster = int(input('Enter the number of Monsters: '))
    base_xp = int(input('Enter the amount of Base XP: '))
    xp_per_hp = int(input('Enter amount of XP per Hit Point: '))
    hit_points = int(input('Enter amount of Hit Points: '))
    bonus_xp = int(input('Enter total amount of Bonus XP: '))

    return num_monster, base_xp, xp_per_hp, hit_points, bonus_xp
    
def get_custom_xp(num_monster: int, base_xp: int, xp_per_hp: int, hit_points: int, bonus_xp: int):
    return (base_xp + (xp_per_hp * hit_points) + bonus_xp) * num_monster

def calculate_xp(xp_dict: dict):
    again = 'y'
    valid = True

    while again.lower() == 'y' and valid == True:
        try:
            print('=' * 40)
            default = input('Default or Custom XP (D/C)? ').lower()
            if default not in ['default', 'd', 'custom', 'c']:
                raise Exception

            if default == 'default':
                num_monster, hit_dice, hit_points, special, exceptional = get_default_input()
            else:
                num_monster, base_xp, xp_per_hp, hit_points, bonus_xp = get_custom_input()

            print()
        except:
            print('ERROR - Invalid Entry: Retry entry\n')
        else:
            if default == 'default':
                xp_amount = get_default_xp(xp_dict, num_monster, hit_dice, hit_points, special, exceptional)
            else:
                xp_amount = get_custom_xp(num_monster, base_xp, xp_per_hp, hit_points, bonus_xp)
            
            print(f'Amount of XP: {xp_amount:,}')

        again = input('Continue (Y/N)? ')

def main():
    xp_dict = build_xp_table()

    calculate_xp(xp_dict)

if __name__ == '__main__':
    main()