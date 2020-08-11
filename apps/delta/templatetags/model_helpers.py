from django import template

register = template.Library()


@register.inclusion_tag("delta/emails/model_table.html", takes_context=True)
def model_as_table(context, model_key=None):
    exclude_fields = ["id"]

    if model_key is None:
        model_key = "object"

    all_fields = context[model_key]._meta.get_fields()
    fields = [f for f in all_fields if f.name not in exclude_fields]
    table_context = {"rows": []}  # type: ignore
    for field in fields:

        try:
            value = str(getattr(context[model_key], field.name))
            if value:
                table_context["rows"].append(
                    {"attr": field.verbose_name, "value": value}
                )
        except AttributeError:
            pass
        # Needs a way to display many_to_many fields.
        except StopIteration:
            pass

    return table_context


@register.inclusion_tag("delta/emails/model_table.html", takes_context=True)
def dict_as_table(context, dict_name=None):
    exclude_fields = ["id"]

    if dict_name is None:
        dict_name = "object"

    dict = {k: v for k, v in context[dict_name].items() if k not in exclude_fields}
    table_context = {"rows": []}  # type: ignore
    for key, value in dict.items():

        table_context["rows"].append({"attr": key, "value": value})

    return table_context


@register.filter
def dic_as_text(dic):
    return "".join([f"{k}: {v}\n" for k, v in dic.items()])
