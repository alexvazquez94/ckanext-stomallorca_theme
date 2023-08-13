
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-

import ckan.lib.helpers as h
import ckan.lib.munge as munge
import ckan.model as model
import ckan.plugins.toolkit as toolkit
import ckanext.dge_scheming.helpers as dh

from ckantoolkit import get_validator

def scheming_validator(fn):
    """
    Decorate a validator for using with scheming.
    """
    fn.is_a_scheming_validator = True
    return fn


"""
PACKAGE VALIDATOR TO AVOID SPECIAL CHARS SCRIPTING
"""
@scheming_validator
def tags_html_detected(field, schema):
    from bs4 import BeautifulSoup

    def validator(key, data, errors, context):
        if errors[key] or 'resources' in str(data):
            return

        value = data.get(key)
        languages = []
        # This is the number of inputs that have implemented this validator EX:title_translated
        prefix = key[0]

        extras = data.get(('__extras',), {})

        for name, text in extras.iteritems():
            if not name.startswith(prefix):
                continue
            if text:
                soup = BeautifulSoup(text, 'html.parser')
                if len(soup.find_all()) > 0 and name.split('-')[0] == prefix:
                    language = config.get('ckan.locale_order')
                    suffix = name.split('-')[1]
                    if suffix in language:
                        errors[(prefix + '-' + suffix,)
                               ] = ['Contiene tag(s) HTML']
                    else:
                        errors[(prefix,)] = ['Contiene tag(s) HTML']

        if value is not missing:
            soup = BeautifulSoup(value, 'html.parser')
            if len(soup.find_all()) > 0:
                errors[key].append('Contiene tag(s) HTML')

    return validator
