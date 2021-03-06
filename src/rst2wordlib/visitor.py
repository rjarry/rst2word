'''
This file is part of docutils

Created on 26 oct. 2010
@author: diabeteman
'''
from docutils import nodes
from rst2wordlib.wrapper import Word, Excel
from rst2wordlib.constants import Constants as CST
from rst2wordlib.constants import getConstant as getCST
import os.path, re

SPACE_REX = re.compile(r"(\s|\n|\r\n|\r)+", re.DOTALL)
ILLEGAL_REX = re.compile(r"(\s|-|'|,|\(|\)|\"|:|;|\?|&|#|%|\+|/|\.|!|\*)+")


class WordTranslator(nodes.NodeVisitor):
    
    def __init__(self, document):
        nodes.NodeVisitor.__init__(self, document)
        self.settings = document.settings
        if self.settings.word_template and not os.path.isabs(self.settings.word_template):
            self.settings.word_template = os.path.join(os.path.abspath(os.curdir), self.settings.word_template)
        elif not self.settings.word_template:
            if self.settings._destination.endswith(".docx"):
                template_extension = ".dotx"
            else:
                template_extension = ".dot"
            self.settings.word_template = get_default_template(template_extension)
        
        self.word = Word(self.settings.word_template)
        
        self.document = document
        self.root_path = os.path.abspath(os.path.dirname(self.document.attributes["source"]))
        self.destination = self.settings._destination
        if not os.path.isabs(self.destination):
            self.destination = os.path.join(os.path.abspath(os.curdir), self.destination)
        
        name, extension = self.destination.rsplit(".", 1)
        if extension == "pdf":
            self.pdf_destination = self.destination
        else:
            self.pdf_destination = None
        
        self.section_level = 0
        self.cur_table_dimensions = (0, 0)
        self.in_table = False
        self.cur_row = 0
        self.cur_column = 0
        self.list_level = 0
        self.in_doc_property = False
        self.doc_property_name = None
        self.property_separator = None
        self.first_property = False
        self.skip_text = False
        self.in_litteral_block = False
        self.in_list = False
        self.in_admonition = False
        self.bookmarks = {}
        self.in_link = False
        self.in_table_head = False
        self.remove_carriage_return = False
        self.sections = [Section()]

    def visit_Text(self, node):
        if self.skip_text: return
        
        text = node.astext()

        if self.in_doc_property and self.doc_property_name:
            if self.property_separator and not self.first_property:
                prop = self.word.getDocProperty(self.doc_property_name)
                text = prop + self.property_separator + text
            
            if self.first_property: 
                self.first_property = False
            
            self.word.setDocProperty(self.doc_property_name, text)
            return
        
        if not self.in_litteral_block:
            text = SPACE_REX.subn(" ", text)[0]
            
        self.word.addText(text)

    def depart_Text(self, node):
        pass

    def visit_abbreviation(self, node):
        pass

    def depart_abbreviation(self, node):
        pass

    def visit_acronym(self, node):
        pass

    def depart_acronym(self, node):
        pass

    def visit_address(self, node):
        pass

    def depart_address(self, node):
        pass

    def visit_admonition(self, node):
        self.in_admonition = True
        node_class = node["classes"][0]
        if node_class in ["error", "attention", "danger"]:
            self.word.setStyle(CST.wdStyleBodyTextIndent)
        elif node_class in ["caution", "warning", "important"]:
            self.word.setStyle(CST.wdStyleBodyTextIndent2)
        else:
            self.word.setStyle(CST.wdStyleBodyTextIndent3)

    def depart_admonition(self, node):
        self.in_admonition = False
        self.word.clearFormatting()

    def visit_attention(self, node):
        pass
    
    def depart_attention(self, node):
        pass

    def visit_attribution(self, node):
        self.word.setStyle(CST.wdStyleBodyText3)

    def depart_attribution(self, node):
        self.word.newParagraph()
        self.word.clearFormatting()

    def visit_author(self, node):
        self.in_doc_property = True
        self.doc_property_name = "Author"
        self.property_separator = ", "

    def depart_author(self, node):
        self.in_doc_property = False
        self.property_separator = None

    def visit_authors(self, node):
        self.first_property = True

    def depart_authors(self, node):
        pass

    def visit_block_quote(self, node):
        self.word.setStyle(CST.wdStyleBodyText2)

    def depart_block_quote(self, node):
        self.word.clearFormatting()

    def visit_bullet_list(self, node):
        if not (self.skip_text or self.in_admonition):
            self.list_level += 1
            if self.list_level > 5:
                self.list_level = 5
            if self.list_level == 1:
                style = CST.wdStyleListBullet
            else:
                style = getCST("wdStyleListBullet%d" % self.list_level)
            self.word.setStyle(style)
            self.in_list = True
            self.remove_carriage_return = False

    def depart_bullet_list(self, node):
        if not (self.skip_text or self.in_admonition):
            self.list_level -= 1
            self.in_list = False
            self.word.clearFormatting()
            if self.in_table:
                self.remove_carriage_return = True

    def visit_caption(self, node):
        self.word.setStyle(CST.wdStyleCaption)

    def depart_caption(self, node):
        self.word.newParagraph()
        self.word.clearFormatting()

    def visit_caution(self, node):
        pass

    def depart_caution(self, node):
        pass

    def visit_citation(self, node):
        pass

    def depart_citation(self, node):
        pass

    def visit_citation_reference(self, node):
        pass

    def depart_citation_reference(self, node):
        pass

    def visit_classifier(self, node):
        pass

    def depart_classifier(self, node):
        pass

    def visit_colspec(self, node):
        pass

    def depart_colspec(self, node):
        pass

    def visit_comment(self, node):
        self.skip_text = True

    def depart_comment(self, node):
        self.skip_text = False

    def visit_compound(self, node):
        pass

    def depart_compound(self, node):
        pass

    def visit_contact(self, node):
        pass

    def depart_contact(self, node):
        pass

    def visit_container(self, node):
        pass

    def depart_container(self, node):
        pass

    def visit_copyright(self, node):
        pass

    def depart_copyright(self, node):
        pass

    def visit_danger(self, node):
        pass

    def depart_danger(self, node):
        pass

    def visit_date(self, node):
        self.in_doc_property = True
        self.doc_property_name = "date"

    def depart_date(self, node):
        self.in_doc_property = False

    def visit_decoration(self, node):
        pass

    def depart_decoration(self, node):
        pass

    def visit_definition(self, node):
        self.word.setStyle(CST.wdStyleNormal)
        self.cur_column += 1

    def depart_definition(self, node):
        if self.remove_carriage_return:
            self.remove_carriage_return = False
            self.word.selection.TypeBackspace()
        if (self.cur_row >= self.cur_table_dimensions[0]):
            return
        else:
            self.word.move("right", CST.wdCell)

    def visit_definition_list(self, node):
        self.in_table = True
        rows, cols = len(node.children), 2
        self.cur_table_dimensions = (rows, cols)
        table = self.word.addTable(rows, cols)
        self.word.formatTable(table, 
                              lateral_padding=self.settings.lateral_padding, 
                              vertical_padding=self.settings.vertical_padding, 
                              border=False)
                              

    def depart_definition_list(self, node):
        self.in_table = False
        self.cur_column = 0
        self.cur_row = 0
        self.word.move("down", CST.wdLine)
        self.word.clearFormatting()

    def visit_definition_list_item(self, node):
        self.cur_column = 0
        self.cur_row += 1

    def depart_definition_list_item(self, node):
        pass

    def visit_description(self, node):
        pass

    def depart_description(self, node):
        pass

    def visit_docinfo(self, node):
        pass

    def depart_docinfo(self, node):
        pass

    def visit_doctest_block(self, node):
        self.word.setStyle(CST.wdStyleHtmlPre)
        self.in_litteral_block = True

    def depart_doctest_block(self, node):
        self.in_litteral_block = False
        self.word.clearFormatting()
        self.word.newParagraph()

    def visit_document(self, node):
        if self.settings.show_gui: 
            self.word.show()
        self.word.setStyle(CST.wdStyleBodyText)

    def depart_document(self, node):
        print "Updating bookmarks..."
        for link in self.word.getHyperlinks():
            try:
                self.bookmarks[link.Address]
                self.word.convertToInternalHyperlink(link)
            except KeyError:
                pass
        print "Updating document fields..."
        self.word.updateFields()

    def visit_emphasis(self, node):
        self.word.setStyle(CST.wdStyleEmphasis)

    def depart_emphasis(self, node):
        self.word.setStyle(CST.wdStyleDefaultParagraphFont)

    def visit_entry(self, node):
        self.cur_column += 1
        if self.in_table_head:
            self.word.setFont("Bold")

    def depart_entry(self, node):
        if self.remove_carriage_return:
            self.remove_carriage_return = False
            self.word.selection.TypeBackspace()
        if (self.cur_row >= self.cur_table_dimensions[0] and 
            self.cur_column >= self.cur_table_dimensions[1]):
            return
        else:
            self.word.move("right", CST.wdCell)

    def visit_enumerated_list(self, node):
        if not (self.skip_text or self.in_admonition):
            self.list_level += 1
            if self.list_level > 5:
                self.list_level = 5
            if self.list_level == 1:
                style = CST.wdStyleListNumber
            else:
                style = getCST("wdStyleListNumber%d" % self.list_level)
            self.word.setStyle(style)
            self.word.resetListStartNumber()
            self.in_list = True

    def depart_enumerated_list(self, node):
        if not (self.skip_text or self.in_admonition):
            self.list_level -= 1
            self.in_list = False
            self.word.clearFormatting()

    def visit_error(self, node):
        pass

    def depart_error(self, node):
        pass

    def visit_field(self, node):
        self.skip_text = True
        field_name = node.children[0].astext()
        field_value = node.children[1].astext()
        self.word.setDocProperty(field_name, field_value)

    def depart_field(self, node):
        self.skip_text = False

    def visit_field_body(self, node):
        pass

    def depart_field_body(self, node):
        pass

    def visit_field_list(self, node):
        pass

    def depart_field_list(self, node):
        pass

    def visit_field_name(self, node):
        pass

    def depart_field_name(self, node):
        pass

    def visit_figure(self, node):
        try:
            figure_align = node["align"]
        except KeyError:
            figure_align = "center"
            
        if figure_align == "center":
            self.word.setAlignment(CST.wdAlignParagraphCenter)
        elif figure_align == "left":
            self.word.setAlignment(CST.wdAlignParagraphLeft)
        elif figure_align == "right":
            self.word.setAlignment(CST.wdAlignParagraphRight)
        else:
            self.word.setAlignment(CST.wdAlignParagraphCenter)

    def depart_figure(self, node):
        self.word.clearFormatting()
    
    def visit_footer(self, node):
        pass

    def depart_footer(self, node):
        pass

    def visit_footnote(self, node):
        pass

    def depart_footnote(self, node):
        pass

    def visit_footnote_reference(self, node):
        pass

    def depart_footnote_reference(self, node):
        pass

    def visit_generated(self, node):
        pass

    def depart_generated(self, node):
        pass

    def visit_header(self, node):
        pass

    def depart_header(self, node):
        pass

    def visit_hint(self, node):
        pass

    def depart_hint(self, node):
        pass

    def visit_image(self, node):
        if isinstance(node.parent, nodes.substitution_definition):
            return
        
        image_path = node["uri"]
        
        if not os.path.isabs(image_path):
            image_path = os.path.join(self.root_path, image_path)
        
        if not isinstance(node.parent, nodes.figure):
            self.word.setAlignment(CST.wdAlignParagraphCenter)
        
        image = self.word.insertImage(os.path.normpath(image_path))
        
        scale = int(self.settings.image_scale)
        try:
            scale *= int(node["scale"]) / 100.0
        except KeyError:
            pass
        
        self.word.scaleImage(image, scale)

    def depart_image(self, node):
        self.word.newParagraph()

    def visit_important(self, node):
        pass

    def depart_important(self, node):
        pass

    def visit_inline(self, node):
        pass

    def depart_inline(self, node):
        pass

    def visit_label(self, node):
        pass

    def depart_label(self, node):
        pass

    def visit_legend(self, node):
        pass

    def depart_legend(self, node):
        pass

    def visit_line(self, node):
        pass

    def depart_line(self, node):
        self.word.newParagraph()

    def visit_line_block(self, node):
        pass

    def depart_line_block(self, node):
        pass

    def visit_list_item(self, node):
        pass

    def depart_list_item(self, node):
        pass

    def visit_literal(self, node):
        self.word.setStyle(CST.wdStyleHtmlCode)

    def depart_literal(self, node):
        self.word.setStyle(CST.wdStyleDefaultParagraphFont)

    def visit_literal_block(self, node):
        self.in_litteral_block = True
        self.word.setStyle(CST.wdStyleHtmlPre)

    def depart_literal_block(self, node):
        self.in_litteral_block = False
        self.word.newParagraph()
        self.word.clearFormatting()

    def visit_note(self, node):
        pass

    def depart_note(self, node):
        pass

    def visit_option(self, node):
        pass

    def depart_option(self, node):
        pass

    def visit_option_argument(self, node):
        pass

    def depart_option_argument(self, node):
        pass

    def visit_option_group(self, node):
        pass

    def depart_option_group(self, node):
        pass

    def visit_option_list(self, node):
        pass

    def depart_option_list(self, node):
        pass

    def visit_option_list_item(self, node):
        pass

    def depart_option_list_item(self, node):
        pass

    def visit_option_string(self, node):
        pass

    def depart_option_string(self, node):
        pass

    def visit_organization(self, node):
        self.in_doc_property = True
        self.doc_property_name = "Company"

    def depart_organization(self, node):
        self.in_doc_property = False

    def visit_paragraph(self, node):
        if self.in_table:
            self.remove_carriage_return = False
        elif not (self.skip_text 
                or self.in_list 
                or self.in_table 
                or self.in_admonition):
            self.word.setStyle(CST.wdStyleBodyText)

    def depart_paragraph(self, node):
        if self.in_table:
            self.remove_carriage_return = True
            self.word.newParagraph()
        elif not (self.skip_text or self.in_table):
            self.word.newParagraph()
            if not (self.in_list or self.in_admonition):
                self.word.clearFormatting()

    def visit_pending(self, node):
        pass

    def depart_pending(self, node):
        pass

    def visit_problematic(self, node):
        pass

    def depart_problematic(self, node):
        pass

    def visit_raw(self, node):
        self.skip_text = True
        
        filename = node["source"]
        if not os.path.isabs(filename):
            filename = os.path.join(self.root_path, filename)
        
        if node["format"] == "excel":
            xl = Excel(os.path.normpath(filename))
            xl.copyCells()
            self.word.pasteExcelTable()
            xl.close()
        elif node["format"] == "powerpoint":
            self.word.addOLEObject(os.path.normpath(filename))
        else:
            f = open(filename, "r")
            content = f.read()
            self.word.setStyle(CST.wdStyleHtmlPre)
            self.word.addText(content)
            self.word.newParagraph()
            self.word.clearFormatting()

    def depart_raw(self, node):
        self.skip_text = False

    def visit_reference(self, node):
        if self.skip_text:
            return
        else:
            self.skip_text = True
            self.in_link = True
            if node.attributes.__contains__("refid"):
                bookmark_id = ILLEGAL_REX.subn("_", node["refid"])[0]
            elif node.attributes.__contains__("refuri"):
                bookmark_id = node["refuri"]
            self.word.insertHyperlink(text=node.astext(), target=bookmark_id)

    def depart_reference(self, node):
        if self.in_link:
            self.skip_text = False
            self.in_link = False

    def visit_revision(self, node):
        pass

    def depart_revision(self, node):
        pass

    def visit_row(self, node):
        self.cur_column = 0
        self.cur_row += 1
    
    def depart_row(self, node):
        pass

    def visit_rubric(self, node):
        pass

    def depart_rubric(self, node):
        pass

    def visit_section(self, node):
        section = Section()
        self.sections[-1].next_child += 1
        section.number = self.sections[-1].next_child
        section.start = self.word.selection.Start
        self.sections.append(section)
        section.title = calcSectionNumber(self.sections)

    def depart_section(self, node):
        section = self.sections.pop()
        section.end = self.word.selection.Start
        self.word.insertBookmark(name=section.title, start=section.start, end=section.end)

    def visit_sidebar(self, node):
        pass

    def depart_sidebar(self, node):
        pass

    def visit_status(self, node):
        pass

    def depart_status(self, node):
        pass

    def visit_strong(self, node):
        self.word.setStyle(CST.wdStyleStrong)

    def depart_strong(self, node):
        self.word.setStyle(CST.wdStyleDefaultParagraphFont)

    def visit_subscript(self, node):
        self.word.setFont("Subscript")

    def depart_subscript(self, node):
        self.word.setStyle(CST.wdStyleDefaultParagraphFont)

    def visit_substitution_definition(self, node):
        self.skip_text = True
        field_name = node["names"][0]
        field_value = node.astext()
        self.word.setDocProperty(field_name, field_value)

    def depart_substitution_definition(self, node):
        self.skip_text = False

    def visit_substitution_reference(self, node):
        self.skip_text = True
        field_name = node.astext()
        self.word.insertField(field_name)

    def depart_substitution_reference(self, node):
        self.skip_text = False

    def visit_subtitle(self, node):
        self.in_title = True
        self.word.setStyle(CST.wdStyleSubtitle)

    def depart_subtitle(self, node):
        self.in_title = False
        self.word.newParagraph()
        self.word.clearFormatting()

    def visit_superscript(self, node):
        self.word.setFont("Superscript")

    def depart_superscript(self, node):
        self.word.setStyle(CST.wdStyleDefaultParagraphFont)

    def visit_system_message(self, node):
        pass

    def depart_system_message(self, node):
        pass

    def visit_table(self, node):
        self.in_table = True
        rows, cols = get_table_size(node)
        self.cur_table_dimensions = (rows, cols)
        table = self.word.addTable(rows, cols)
        if "no-format" in node["classes"]:
            self.word.formatTable(table, 
                                  lateral_padding=self.settings.lateral_padding, 
                                  vertical_padding=self.settings.vertical_padding, 
                                  border=False)
        else:
            self.word.formatTable(table=table, 
                                  lateral_padding=self.settings.lateral_padding, 
                                  vertical_padding=self.settings.vertical_padding, 
                                  border=True, 
                                  first_row_bg_color=CST.wdColorGray15)

    def depart_table(self, node):
        self.in_table = False
        self.cur_column = 0
        self.cur_row = 0
        self.word.move("down", CST.wdLine)
        self.word.clearFormatting()

    def visit_target(self, node):
        if self.skip_text:
            return
        try:
            bookmark_id = ILLEGAL_REX.subn("_", node["refid"])[0]
            self.bookmarks[bookmark_id] = bookmark_id
            self.word.insertBookmark(bookmark_id)
        except KeyError:
            pass
        
    def depart_target(self, node):
        pass

    def visit_tbody(self, node):
        pass

    def depart_tbody(self, node):
        pass

    def visit_term(self, node):
        self.cur_column += 1
        self.word.setStyle(CST.wdStyleNormal)
        self.word.setFont("Bold")
        self.word.setAlignment(CST.wdAlignParagraphRight)

    def depart_term(self, node):
        if self.remove_carriage_return:
            self.remove_carriage_return = False
            self.word.selection.TypeBackspace()
        self.word.setStyle(CST.wdStyleDefaultParagraphFont)
        self.word.move("right", CST.wdCell)

    def visit_tgroup(self, node):
        pass

    def depart_tgroup(self, node):
        pass

    def visit_thead(self, node):
        self.in_table_head = True

    def depart_thead(self, node):
        self.in_table_head = False

    def visit_tip(self, node):
        pass

    def depart_tip(self, node):
        pass

    def visit_title(self, node):
        if isinstance(node.parent, nodes.topic):
            # title of table of contents
            text = node.astext()
            self.word.setStyle(CST.wdStyleSubtitle)
            self.word.addText(text)
            
        elif isinstance(node.parent, nodes.sidebar):
            pass
        elif isinstance(node.parent, nodes.Admonition):
            self.in_admonition = True
            self.word.setFont("Bold")
        elif isinstance(node.parent, nodes.table):
            pass # caption
        elif isinstance(node.parent, nodes.document):
            # document title
            self.doc_property_name = "Title"
            self.in_doc_property = True
        else:
            assert isinstance(node.parent, nodes.section)
            level = len(self.sections) - 1 # we do not take the first section as it is dummy
            if level > 9 : level = 9
            self.word.setStyle(getCST("wdStyleHeading%d" % level))
            bookmark_id = ILLEGAL_REX.subn("_", node.astext())[0]
            self.sections[-1].title = self.sections[-1].title + "_" + bookmark_id 


    def depart_title(self, node):
        self.word.newParagraph()
        self.in_doc_property = False
        if self.in_admonition:
            self.word.setStyle(CST.wdStyleDefaultParagraphFont)
        else:
            self.word.clearFormatting()

    def visit_title_reference(self, node):
        pass

    def depart_title_reference(self, node):
        pass

    def visit_topic(self, node):
        if "contents" in node["classes"]:
            self.skip_text = True

    def depart_topic(self, node):
        if "contents" in node["classes"]:
            self.word.insertTableOfContents(self.settings.toc_depth)
            self.word.newParagraph()
            self.skip_text = False
        

    def visit_transition(self, node):
        self.skip_text = True

    def depart_transition(self, node):
        self.word.insertPageBreak()
        self.skip_text = False

    def visit_version(self, node):
        pass

    def depart_version(self, node):
        pass

    def visit_warning(self, node):
        pass

    def depart_warning(self, node):
        pass
    

#################################################################
#### UTIL METHODS ###############################################
#################################################################

def get_table_size(node):
    r_head, c_head = extract_sizes(node, thead=True)
    r_body, c_body = extract_sizes(node, thead=False)
    rows = r_head + r_body
    cols = max(c_head, c_body)
    return rows, cols
    
def extract_sizes(node, thead=True):
    if thead: tag = "thead"
    else:     tag = "tbody"
    rows, cols = 0, 0
    for c in node.children:
        if c.tagname == "tgroup":
            for cc in c.children:
                if cc.tagname == tag:
                    rows = len(cc.children)
                    cols = len(cc.children[0].children)
                    break
            break
    return rows, cols

def get_default_template(extension=".dotx"):
    import sys
    return os.path.normpath( sys.prefix + "/rst2word/templates/rst2word" + extension)
    
    
class Hyperlink:
    start = None
    end = None
    target = None
    text = None

class Section:
    start = None
    end = None
    title = None
    number = 1
    next_child = 0
    
def calcSectionNumber(sections):
    number = "T"
    for s in sections[1:]: # we ignore the first dummy section
        number += "_%d" % s.number
    return number
