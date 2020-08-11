from django.forms.models import model_to_dict


def model_to_dict_verbose(instance, exclude=("id")):
    dic = model_to_dict(instance, exclude=exclude)
    verbose_name = {f.name: f.verbose_name for f in instance._meta.fields}
    fields = {f.name: f for f in instance._meta.fields}
    verbose_dic = {}
    for k, v in dic.items():
        field = fields[k]
        key = field.verbose_name
        value = str(v)
        if hasattr(field, 'choices') and fields[k].choices:
            value = dict(fields[k].choices).get(v, "")

        if field.get_internal_type() in ["DateField"]:
            if v:
                value = v.strftime("%d/%m/%Y")
        verbose_dic[key] = value


    return verbose_dic

