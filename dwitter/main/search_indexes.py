#!/usr/bin/env python
# -*- coding: utf-8 -*-

from haystack import indexes
from dwitter.main.models import Member

class MemberIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    
    def get_model(self):
        return Member
