#!/usr/bin/python
# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Products.CMFPlone.browser.search import Search
from AccessControl import getSecurityManager
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.app.uuid.utils import uuidToCatalogBrain
from plone import api

class AdvancedSearchView(BrowserView, Search):
    """
    Adding to Search view
    """

    def checkUserPermission(self):
        sm = getSecurityManager()
        if sm.checkPermission(ModifyPortalContent, self.context):
            return True
        return False

    def getAdvancedButtonQuery(self):
        params = self.request.form.items()

        registry = getUtility(IRegistry)
        searchFiltersRecord = registry.get('advancedsearch.fields', None)
        q = ""

        if searchFiltersRecord:
            advancedfields = list(searchFiltersRecord)
            advancedfields.append("SearchableText")
            """advancedfields.append("sort_on")"""
            try:
                q = "&".join(["%s=%s" %(param,value.decode('utf-8').encode('ascii', 'ignore')) for param,value in params if param in advancedfields and value])
            except:
                pass

        return q

    def getSearchFilters(self, lang='nl'):
        searchFilters = []
        registry = getUtility(IRegistry)

        if lang == "nl":
            searchFiltersRecord = ['163baacdad1f49e3acf7fc577547a9ae']
        else:
            searchFiltersRecord = ['8821485ba9134088b97ae8d4726d3da3']

        if searchFiltersRecord:
            filters = list(searchFiltersRecord)
            if filters:
                for uid in filters:
                    item = uuidToCatalogBrain(uid)
                    if item:
                        searchFilters.append({"name": item.Title, "path": item.getPath()})
                        
        return searchFilters

    def getExtraFilters(self):
        params = self.request.form.items()
        extra_filters = []

        # Needs fix
        widget_fields = ['sortable_creator_name', 'association_subject', 'acquisition_method', 'creator_role', 'object_qualifier', 'sortable_creator_name', 'object_name']


        new_params = []
        for k, v in params:
            if k != "path":
                new_params.append((k,v))
            else:
                if type(v) is list:
                    for p in v:
                        new_params.append(('path:list', p))
                else:
                    new_params.append((k,v))

        params = new_params

        registry = getUtility(IRegistry)
        searchFiltersRecord = registry.get('advancedsearch.fields', None)

        if searchFiltersRecord:
            advancedfields = list(searchFiltersRecord)
            advancedfields.append('path')
            """advancedfields.append('sort_on')"""

            for param, value in params:
                if param in advancedfields:
                    if value:
                        if type(value) == list:
                            continue
                        if param in widget_fields:
                            list_fields = value.split("_")
                            curr = 0
                            for field in list_fields:
                                curr += 1
                                q = "&".join(["%s=%s" %(p, v) for p, v in params if p != param and p not in ['created']])

                                new_list_field = [f for f in list_fields if f != field]
                                new_string = "_".join(new_list_field)
                                q += "&%s=%s" %(param, new_string)

                                search_filter = {}
                                if curr > 1:
                                    search_filter["param"] = ''
                                else:
                                    search_filter["param"] = param
                                search_filter["value"] = field
                                search_filter["link"] = self.context.absolute_url()+"/%s/@@search?%s" %(getattr(self.context, 'language', ''), q)
                                extra_filters.append(search_filter)
                        else:
                            q = "&".join(["%s=%s" %(p, v) for p, v in params if p != param and p not in ['created']])
                            search_filter = {}
                            search_filter["param"] = param
                            search_filter["value"] = value
                            search_filter["link"] = self.context.absolute_url()+"/%s/@@search?%s" %(getattr(self.context, 'language', ''), q)
                            extra_filters.append(search_filter) 
        return extra_filters

    def getSortFields(self):
        sort_filters = [{"name":"sort_on", "options": ['sortable_creator_name', 'sortable_object_number', 'sortable_production_date', 'sortable_title']}]
        return sort_filters

    def getAdvancedFields(self):

        context_url = self.context.absolute_url()

        advanced_widgets = {
            'sortable_creator_name': {
                'data':'{"orderable": true, "vocabularyUrl": "%s/@@getVocabulary?name=collective.object.creatorname", "initialValues": {}, "separator": "_"}' % (context_url)
            },
            'object_material': {
                'data':'{"orderable": true, "vocabularyUrl": "%s/@@getVocabulary?name=collective.object.objectmaterial", "initialValues": {}, "separator": "_"}' % (context_url)
            },
            'object_technique': {
                'data':'{"orderable": true, "vocabularyUrl": "%s/@@getVocabulary?name=collective.object.objecttechnique", "initialValues": {}, "separator": "_"}' % (context_url)
            },
            'object_name': {
                'data':'{"orderable": true, "vocabularyUrl": "%s/@@getVocabulary?name=collective.object.objectname", "initialValues": {}, "separator": "_"}' % (context_url)
            }
        }
        
        searchFilters = []
        registry = getUtility(IRegistry)
        searchFiltersRecord = registry.get('advancedsearch.fields', None)
        if searchFiltersRecord:
            filters = list(searchFiltersRecord)
            if filters:
                for advanced_filter in filters:
                    if advanced_filter != "":
                        is_widget = False
                        data_select = ""
                        if advanced_filter in advanced_widgets:
                            is_widget = True
                            data_select = advanced_widgets[advanced_filter]['data']

                        new_filter = {
                            "name": advanced_filter,
                            "is_widget": is_widget,
                            "select2_data": data_select
                        }

                        searchFilters.append(new_filter)
                    else:
                        continue
            else:
                return searchFilters

        return searchFilters

