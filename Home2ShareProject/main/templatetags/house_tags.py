from django import template
register = template.Library()

@register.inclusion_tag('tag_show_house_list.html')
def show_house_list(house_list, logged_user, multiline=True, user_buttons=True):
    context = {
        'house_list': house_list,
        'logged_user' : logged_user,
        'multiline' : multiline,
        'user_buttons' : user_buttons
    }

    return context
