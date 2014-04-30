from abc import abstractmethod

import codecs
import os.path
import fableme.db.booktemplates as fables
import fableme.utils as utils
import sys

class TemplateLoader(object):
    """
    A 'loader' class is a class that loads a template from a text file,
    replaces tags, and saves a formatted (PDF, ePub, HTML) document.
    
    A 'loader' takes in input a 'formatter' (see TextFormatter) to
    select the formatting technology to be used (ie: PDF, ePub)
    
    Example of use:
    
            template = loader.SimpleLoader(fable_id, tlang, character)
            template.build() 
            template.save()
    
    """
    def __init__(self, fable_id, lang, character):
        """
        Initialize the template loader
        - fable_id: Fable id
        - lang: Fable language
        - character: A character as in fableme/db/character.py
        """
        self._fable_id = fable_id
        self._set_variables(lang, character)
    
    @abstractmethod
    def build(self):
        return NotImplemented
    
    @abstractmethod
    def save(self):
        return NotImplemented
    
    def _readFile(self):
        """
            1) Reads the file from _filename
            2) Replaces tags based on variables passed
            3) Builds paragraphs
            
            return True if the file was correctly read
        """
        fileReadOk = True
        fileFullPath = self._get_resources_path_to(self._filename)
        print '-- Reading file ' + fileFullPath
        try:
            fileobj = codecs.open(fileFullPath, "r", "utf-8")
            self._fabletemplate = unicode(fileobj.read())
            filecontents = self._replace_tags()
            fileobj.close()
            self.paras = filecontents.split('\n')
            print '-- The file has ' + str(len(self.paras)) + ' paragraphs.'
        except IOError:
            print '*** Critical error opening %s' % fileFullPath
            print '*** ', sys.exc_info()
            fileReadOk = False
        return fileReadOk
    
    def _get_resources_path(self):
        fable_dir = self._template['template_dir']
        lang_code = self._language.language_code()
        filepath = utils.BasicUtils.get_from_relative_resources(fable_dir)
        if (lang_code != "EN"):
            filepath = os.path.join(filepath, lang_code)
        return utils.BasicUtils.normalize_path(filepath)
    
    def _get_resources_path_to(self, filename):
        return os.path.join(self._get_resources_path(), filename)

    def _get_resources_path_lang(self):
        fable_dir = self._template['template_dir']
        filepath_en = utils.BasicUtils.get_from_relative_resources(fable_dir)
        finalpath = os.path.normpath(filepath_en)
        return finalpath
        
    def _set_variables(self, lang, character):
        self._language = self._set_language(self._fable_id, lang)
        self._template = fables.get_book_template(self._fable_id)
        self._filename = self._template['template_text_file']
        self._pdffile = utils.BasicUtils.get_output_path(self._filename[:-4] + '_' + self._language.language_code() + '.pdf')
        self._title = self._template[self._language.get_title_key()]
        try:
            print '-- Creating fable = ' + self._title
        except:
            print '-- Creating fable document'
        self._character = character
        self.fable_doc = None
        self.chapters = []

    
    
    
    