from django import template
register = template.Library()

@register.inclusion_tag('delta/emails/model_table.html', takes_context=True)
def model_as_table(context, model_key=None):
    exclude_fields = ["id"]

    if model_key is None:
        model_key = 'object'


    fields = context[model_key]._meta.get_fields()
    fields = [f for f in fields if f.name not in exclude_fields]
    table_context = {'rows': []}
    for field in fields:

        try:
            value = str(getattr(context[model_key], field.name))
            if value:
                table_context['rows'].append({'attr': field.verbose_name,
                                              'value': value})
        except AttributeError:
            pass
        # Needs a way to display many_to_many fields.
        except StopIteration:
            pass

    return table_context