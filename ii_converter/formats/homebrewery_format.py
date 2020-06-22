import math
import re
# Converter implementation for Homebrewery-compatible markdown.
# Displays as monster stat block.

# Markdown strings for interpolation
h2_field = '___\n> ## {0}'  # h2
h3_field = '___\n> ### {0}'  # h3
italics_field = '\n> *{0}*'  # italics
bold_field = '\n> - **{0}** {1}'  # bold
italics_bold_field = '\n> ***{0}*** {1}'
notes_field = ' {}'  # plaintext
blank = '___'
endl = '\n'
endtag = endl + '>'
endtag_blank = endtag + blank
blank_endl = blank + endl

# Constants reference
list_fields = [
    'DamageVulnerabilities',
    'DamageResistances',
    'DamageImmunities',
    'ConditionImmunities',
    'Senses',
    'Languages'
]

cr_to_xp_dict = {
    '0': '10',
    '1/8': '25',
    '1/4': '50',
    '1/2': '100',
    '1': '200',
    '2': '450',
    '3': '700',
    '4': '1,100',
    '5': '1,800',
    '6': '2,300',
    '7': '2,900',
    '8': '3,900',
    '9': '5,000',
    '10': '5,900',
    '11': '7,200',
    '12': '8,400',
    '13': '10,000',
    '14': '11,500',
    '15': '13,000',
    '16': '15,000',
    '17': '18,000',
    '18': '20,000',
    '19': '22,000',
    '20': '25,000',
    '21': '33,000',
    '22': '41,000',
    '23': '50,000',
    '24': '62,000',
    '25': '75,000',
    '26': '90,000',
    '27': '105,000',
    '28': '120,000',
    '29': '135,000',
    '30': '155,000',
}


def has_field(keys, field):
    return field in keys


def has_field_list(obj, field):
    # For fields that must exist and have elements, e.g. DamageVulnerabilities
    return has_field(obj.keys(), field) and len(obj[field])


def num_to_modifier(num):
    # Adds + to modifier if positive
    if num >= 0:
        return '+{}'.format(num)
    else:
        return str(num)


def stat_to_modifier(stat):
    # E.g. 12 becomes +1
    modifier = math.floor((stat - 10) / 2)
    return num_to_modifier(modifier)


def cr_to_xp(cr):
    if has_field(cr_to_xp_dict.keys(), cr):
        return cr_to_xp_dict[cr]
    else:
        return ''


def spaces_before_capital(string):
    return re.sub(r"(\w)([A-Z])", r"\1 \2", string)


def format_skill(skill):
    return '{0} {1}'.format(skill['Name'], num_to_modifier(skill['Modifier']))


def format_field_list(obj, field):
    # Joins field elements in line with commas
    if has_field_list(obj, field):
        text = '; '
        text = text.join(obj[field])
        return bold_field.format(spaces_before_capital(field), text)

    return ''


def map_content_list(iter):
    # Formats then joins Name:Content pairs
    content_mapped = endtag

    def format_content(iter_obj):
        # Breaks down Name and Content block
        name = iter_obj['Name'] if iter_obj['Name'].endswith(
            '.') else '{}.'.format(iter_obj['Name'])  # add period

        content = re.sub(r'\n', '\n>', iter_obj['Content'])
        content = re.sub(r"/\n\.\n/gim", r"\n>\n> ", content)
        content = re.sub(r"/\n[^> ]/gim", r"\n> ", content)

        return italics_bold_field.format(name, content)

    return content_mapped.join(map(format_content, iter))


def get_markdown(obj):
    # Main function
    obj_keys = obj.keys()

    # NAME AND TYPE
    result = h2_field.format(obj['Name'])
    if has_field(obj_keys, 'Type'):
        result += italics_field.format(obj['Type'])

    result += endtag_blank

    # AC, HP, SPEED
    result += bold_field.format('Armor Class', obj['AC']['Value'])
    if has_field(obj['AC'], 'Notes'):
        result += notes_field.format(obj['AC']['Notes'])

    result += bold_field.format('Hit Points', obj['HP']['Value'])
    if has_field(obj['HP'].keys(), 'Notes'):
        result += notes_field.format(obj['HP']['Notes'])

    result += bold_field.format('Speed', ', '.join(obj['Speed']) or '0 ft.')
    result += endtag_blank

    # ABILITY SCORES
    result += '\n>|STR|DEX|CON|INT|WIS|CHA|'
    result += '\n>|:---:|:---:|:---:|:---:|:---:|:---:|'
    result += '\n>|'

    for ability in obj['Abilities']:
        stat = obj['Abilities'][ability]
        modifier = stat_to_modifier(stat)

        result += '{0} ({1})|'.format(stat, modifier)

    result += endtag_blank

    # SAVES, SKILLS, SENSES, DAMAGE MODIFIERS, LANGUAGES, CR
    if has_field_list(obj, 'Saves'):
        sep_comma = ', '
        saves_result = sep_comma.join(
            map(lambda save: format_skill(save), obj['Saves']))
        result += bold_field.format('Saving Throws', saves_result)

    if has_field_list(obj, 'Skills'):
        sep_comma = ', '
        skills_result = sep_comma.join(
            map(lambda skill: format_skill(skill), obj['Skills']))
        result += bold_field.format('Skills', skills_result)

    for field in list_fields:
        result += format_field_list(obj, field)

    if has_field(obj_keys, 'Challenge'):
        cr_field = '{0} ({1} xp)'.format(
            obj['Challenge'] or '?', cr_to_xp(obj['Challenge']) or '?')
        result += bold_field.format('Challenge', cr_field)

    result += endtag_blank

    # TRAITS
    if has_field_list(obj, 'Traits'):
        result += map_content_list(obj['Traits'])
        result += endtag_blank

    # ACTIONS
    if has_field_list(obj, 'Actions'):
        result += h3_field.format('Actions')
        result += map_content_list(obj['Actions'])
        result += endtag_blank

    if has_field_list(obj, 'Reactions'):
        result += h3_field.format('Reactions')
        result += map_content_list(obj['Reactions'])
        result += endtag_blank

    if has_field_list(obj, 'LegendaryActions'):
        result += h3_field.format('Legendary Actions')
        result += map_content_list(obj['LegendaryActions'])
        result += endtag_blank

    result += endl
    return result


def get_markdown_wide(obj):
    # Prepends tag for wide monster statblocks to default markdown
    wide_result = blank_endl
    wide_result += get_markdown(obj)
    return wide_result
