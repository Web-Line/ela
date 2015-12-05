from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils import html

register = Library()


@register.filter(name='file_icon')
def icon_type(value):
    file_type = value.split('.')[-1]
    html_icon = '<i class="fa {}"></i>'
    IMAGE_ICON = html.format_html(html_icon, 'fa-file-image-o')
    SOUND_ICON = html.format_html(html_icon, 'fa-file-audio-o')
    VIDEO_ICON = html.format_html(html_icon, 'fa-file-video-o')
    PDF_ICON = html.format_html(html_icon, 'fa-file-pdf-o')
    WORD_ICON = html.format_html(html_icon, 'fa-file-word-o')
    EXCEL_ICON = html.format_html(html_icon, 'fa-file-excel-o')
    POWERPOINT_ICON = html.format_html(html_icon, 'fa-file-powerpoint-o')
    TEXT_ICON = html.format_html(html_icon, 'fa-file-text-o')
    ZIP_ICON = html.format_html(html_icon, 'fa-file-archive-o')
    file_type_dic = {'png': 'img', 'jpg': 'img', 'pdf': PDF_ICON,
                     'gif': IMAGE_ICON, 'docx': WORD_ICON, 'xlsx': EXCEL_ICON,
                     'doc': WORD_ICON, 'ppt': POWERPOINT_ICON, 'zip': ZIP_ICON,
                     'rar': ZIP_ICON, 'txt': TEXT_ICON, 'mp4': VIDEO_ICON,
                     'fly': VIDEO_ICON, 'mp3': SOUND_ICON}
    return file_type_dic[file_type]
