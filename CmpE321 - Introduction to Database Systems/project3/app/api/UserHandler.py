from flask_restful import Resource
from flask import Markup

class UserHandler(Resource):

        
    def generate_form_response(self,
                               title,
                               form,
                               exclude=[]):
        list_items = "\n".join(['    <li>%s: %s</li>'%(i, form[i]) for i in form if i not in exclude and i != 'formType'])
        return Markup(f"{title}:\n<ul>\n{list_items}\n</ul>")

    def draw_table_response(self,
                            title,
                            column_names,
                            response):
                            
        get_row = lambda items, tag: "<tr>%s</tr>"%"".join(map(lambda x: f"<{tag}>{x}</{tag}>", items))
        table = f"{get_row(column_names, 'th')}{''.join(map(lambda items: get_row(items, 'td'), response))}"
        return Markup(f"{title}:\n<table>\n{table}\n</table>")
