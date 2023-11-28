DAL_VIEW_PY = """# generated by appcreator
from django.db.models import Q
from dal import autocomplete
from . models import (
{%- for x in data %}
    {{ x.model_name }},
{%- endfor %}
)

{% for x in data %}
class {{ x.model_name }}AC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = {{ x.model_name }}.objects.all()

        if self.q:
            qs = qs.filter(
                Q(legacy_id__icontains=self.q) |
                Q({{ x.model_representation }}__icontains=self.q)
            )
        return qs

{% endfor %}
"""

DAL_URLS_PY = """# generated by appcreator
from django.urls import path
from . import dal_views

app_name = '{{ app_name }}'
urlpatterns = [
{%- for x in data %}
    path(
        "{{ x.model_name|lower }}-autocomplete",
        dal_views.{{ x.model_name}}AC.as_view(),
        name='{{ x.model_name|lower }}-autocomplete'
    ),
{%- endfor %}
]
"""


APP_PY = """
from django.apps import AppConfig
class {{ app_name|title }}Config(AppConfig):
    name = '{{ app_name }}'
"""


ADMIN_PY = """# generated by appcreator
from django.contrib import admin
from . models import (
{%- for x in data %}
    {{ x.model_name }},
{%- endfor %}
)
{%- for x in data %}
admin.site.register({{ x.model_name }})
{%- endfor %}
"""


URLS_PY = """# generated by appcreator
from django.urls import path
from . import views

app_name = '{{ app_name }}'
urlpatterns = [
{%- for x in data %}
    path(
        "{{ x.model_name|lower }}/",
        views.{{ x.model_name}}ListView.as_view(),
        name='{{ x.model_name|lower }}_browse'
    ),
    path(
        "{{ x.model_name|lower }}/detail/<int:pk>",
        views.{{ x.model_name}}DetailView.as_view(),
        name='{{ x.model_name|lower }}_detail'
    ),
    path(
        "{{ x.model_name|lower }}/create/",
        views.{{ x.model_name}}Create.as_view(),
        name='{{ x.model_name|lower }}_create'
    ),
    path(
        "{{ x.model_name|lower }}/edit/<int:pk>",
        views.{{ x.model_name}}Update.as_view(),
        name='{{ x.model_name|lower }}_edit'
    ),
    path(
        "{{ x.model_name|lower }}/delete/<int:pk>",
        views.{{ x.model_name}}Delete.as_view(),
        name='{{ x.model_name|lower }}_delete'),
{%- endfor %}
]
"""

FILTERS_PY = """# generated by appcreator
import django_filters
from dal import autocomplete

try:
    from vocabs.models import SkosConcept
except ModuleNotFoundError:
    pass
from . models import (
{%- for x in data %}
    {{ x.model_name }},
{%- endfor %}
)

{% for x in data %}
class {{ x.model_name }}ListFilter(django_filters.FilterSet):
    legacy_id = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text={{ x.model_name}}._meta.get_field('legacy_id').help_text,
        label={{ x.model_name}}._meta.get_field('legacy_id').verbose_name
    )
    {%- for y in x.model_fields %}
    {%- if y.field_type == 'CharField' %}
    {{y.field_name}} = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text={{ x.model_name}}._meta.get_field('{{y.field_name}}').help_text,
        label={{ x.model_name}}._meta.get_field('{{y.field_name}}').verbose_name
    )
    {%- endif %}
    {%- if y.field_type == 'TextField' %}
    {{y.field_name}} = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text={{ x.model_name}}._meta.get_field('{{y.field_name}}').help_text,
        label={{ x.model_name}}._meta.get_field('{{y.field_name}}').verbose_name
    )
    {%- endif %}
    {%- if y.related_class == 'SkosConcept' %}
    {{y.field_name}} = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            collection__name="{{y.field_name}}"
        ),
        help_text={{x.model_name}}._meta.get_field('{{y.field_name}}').help_text,
        label={{x.model_name}}._meta.get_field('{{y.field_name}}').verbose_name,
        widget=autocomplete.Select2Multiple(
            url="/vocabs-ac/specific-concept-ac/{{y.field_name}}",
            attrs={
                'data-placeholder': 'Autocomplete ...',
                'data-minimum-input-length': 2,
                },
        )
    )
    {%- elif y.field_type == 'ManyToManyField' %}
    {{y.field_name}} = django_filters.ModelMultipleChoiceFilter(
        queryset={{y.related_class}}.objects.all(),
        help_text={{x.model_name}}._meta.get_field('{{y.field_name}}').help_text,
        label={{x.model_name}}._meta.get_field('{{y.field_name}}').verbose_name,
        widget=autocomplete.Select2Multiple(
            url="{{ app_name }}-ac:{{y.related_class|lower}}-autocomplete",
        )
    )
    {%- elif y.field_type == 'ForeignKey' %}
    {{y.field_name}} = django_filters.ModelMultipleChoiceFilter(
        queryset={{y.related_class}}.objects.all(),
        help_text={{x.model_name}}._meta.get_field('{{y.field_name}}').help_text,
        label={{x.model_name}}._meta.get_field('{{y.field_name}}').verbose_name,
        widget=autocomplete.Select2Multiple(
            url="{{ app_name }}-ac:{{y.related_class|lower}}-autocomplete",
        )
    )
    {%- endif %}
    {%- endfor %}

    class Meta:
        model = {{ x.model_name }}
        fields = [
            'id',
            'legacy_id',
            {% for y in x.model_fields %}
            {%- if y.field_type == 'DateRangeField' %}
            {%- else %}'{{ y.field_name }}',
            {%- endif %}
            {% endfor %}]

{% endfor %}
"""

FORMS_PY = """# generated by appcreator
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import AccordionGroup
from crispy_bootstrap5.bootstrap5 import BS5Accordion

try:
    from vocabs.models import SkosConcept
except ModuleNotFoundError:
    pass
from . models import (
{%- for x in data %}
    {{ x.model_name }},
{%- endfor %}
)

{% for x in data %}
class {{ x.model_name }}FilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super({{ x.model_name }}FilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.form_tag = False
        self.layout = Layout(
            BS5Accordion(
                AccordionGroup(
                    'Advanced search',
                    'id',
                    {% for y in x.model_fields %}
                    {% if y.field_type == 'DateRangeField' or y.field_type == 'id' %}
                    {% else %}'{{ y.field_name }}',
                    {%- endif %}
                    {%- endfor %}
                    css_id="more"
                    ),
                AccordionGroup(
                    'admin',
                    'legacy_id',
                    css_id="admin_search"
                    ),
                )
            )


class {{ x.model_name }}Form(forms.ModelForm):

    {%- for y in x.model_fields %}
    {%- if y.related_class == 'SkosConcept' and y.field_type == 'ForeignKey'%}
    {{y.field_name}} = forms.ModelChoiceField(
        required=False,
        label="{{y.field_verbose_name}}",
        queryset=SkosConcept.objects.filter(collection__name="{{y.field_name}}")
    )
    {%- elif y.related_class == 'SkosConcept' and y.field_type == 'ManyToManyField'%}
    {{y.field_name}} = forms.ModelMultipleChoiceField(
        required=False,
        label="{{y.field_verbose_name}}",
        queryset=SkosConcept.objects.filter(collection__name="{{y.field_name}}")
    )
    {%- endif -%}
    {% endfor %}

    class Meta:
        model = {{ x.model_name }}
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super({{ x.model_name }}Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)

{% endfor %}
"""


TABLES_PY = """# generated by appcreator
import django_tables2 as tables

from browsing.browsing_utils import MergeColumn
from . models import (
{%- for x in data %}
    {{ x.model_name }},
{%- endfor %}
)
{% for x in data %}

class {{ x.model_name }}Table(tables.Table):

    id = tables.LinkColumn(verbose_name='ID')
    merge = MergeColumn(verbose_name='keep | remove', accessor='pk')
    {%- for y in x.model_fields %}
    {%- if y.field_type == 'ManyToManyField' %}
    {{ y.field_name }} = tables.columns.ManyToManyColumn()
    {%- endif %}
    {%- endfor %}

    class Meta:
        model = {{ x.model_name }}
        sequence = ('id',)
        attrs = {"class": "table table-responsive table-hover"}
{% endfor %}
"""

VIEWS_PY = """# generated by appcreator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from . filters import (
{%- for x in data %}
    {{ x.model_name }}ListFilter,
{%- endfor %}
)
from . forms import (
{%- for x in data %}
    {{ x.model_name }}Form,
    {{ x.model_name }}FilterFormHelper,
{%- endfor %}
)
from . tables import (
{%- for x in data %}
    {{ x.model_name }}Table,
{%- endfor %}
)
from . models import (
{%- for x in data %}
    {{ x.model_name }},
{%- endfor %}
)
from browsing.browsing_utils import (
    GenericListView, BaseCreateView, BaseUpdateView, BaseDetailView
)

{% for x in data %}
class {{ x.model_name }}ListView(GenericListView):

    model = {{ x.model_name }}
    filter_class = {{ x.model_name }}ListFilter
    formhelper_class = {{ x.model_name }}FilterFormHelper
    table_class = {{ x.model_name }}Table
    init_columns = [
        'id', {%- if x.model_representation != 'nan' %} '{{ x.model_representation }}', {%- endif %}
    ]
    enable_merge = True


class {{ x.model_name }}DetailView(BaseDetailView):

    model = {{ x.model_name }}
    template_name = 'browsing/generic_detail.html'


class {{ x.model_name }}Create(BaseCreateView):

    model = {{ x.model_name }}
    form_class = {{ x.model_name }}Form

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super({{ x.model_name }}Create, self).dispatch(*args, **kwargs)


class {{ x.model_name }}Update(BaseUpdateView):

    model = {{ x.model_name }}
    form_class = {{ x.model_name }}Form

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super({{ x.model_name }}Update, self).dispatch(*args, **kwargs)


class {{ x.model_name }}Delete(DeleteView):
    model = {{ x.model_name }}
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('{{ app_name }}:{{ x.model_name|lower }}_browse')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super({{ x.model_name }}Delete, self).dispatch(*args, **kwargs)

{% endfor %}
"""

MODELS_PY = """# generated by appcreator

from django.db import models
from django.urls import reverse
from next_prev import next_in_order, prev_in_order
try:
    from vocabs.models import SkosConcept
except ModuleNotFoundError:
    pass
from browsing.browsing_utils import model_to_dict


def set_extra(self, **kwargs):
    self.extra = kwargs
    return self


models.Field.set_extra = set_extra

{% for x in data %}
class {{ x.model_name }}(models.Model):
    {% if x.model_helptext %}\""" {{ x.model_helptext }} \"""{% endif %}
    legacy_id = models.CharField(
        max_length=300, blank=True,
        verbose_name="Legacy ID"
        )
    {%- for y in x.model_fields %}
    {%- if y.field_type == 'DateRangeField' %}
    {{ y.field_name }} = {{ y.field_type}}(
    {%- else %}
    {{ y.field_name }} = models.{{ y.field_type}}(
    {%- endif %}
        {%- if y.field_type == 'DecimalField' %}
        max_digits=19,
        decimal_places=10,
        {%- endif %}
        {%- if y.field_type == 'BooleanField' %}
        default=False,
        {%- endif %}
        {%- if y.field_type == 'CharField' %}
        {%- if y.choices %}
        choices={{ y.choices }},
        {%- endif %}
        max_length=250,
        blank=True,
        {%- elif y.field_type == 'TextField' %}
        blank=True, null=True,
        {%- elif y.field_type == 'ForeignKey' %}
        {%- if y.related_class == 'SkosConcept' %}
        {{ y.related_class }},
        {%- else %}
        "{{ y.related_class }}",
        {%- endif %}
        related_name='{{ y.related_name }}',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        {%- elif y.field_type == 'ManyToManyField' %}
        {%- if y.related_class == 'SkosConcept' %}
        {{ y.related_class }},
        {%- else %}
        "{{ y.related_class }}",
        {%- endif %}
        {%- if y.through %}
        through='{{ y.through }}',
        {%- endif %}
        related_name='{{ y.related_name }}',
        blank=True,
        {%- else %}
        blank=True, null=True,
        {%- endif %}
        verbose_name="{{ y.field_verbose_name }}",
        help_text="{{ y.field_helptext }}",
    ).set_extra(
        is_public={{ y.field_public }},
        {%- if y.value_from %}
        data_lookup="{{ y.value_from }}",
        {%- endif %}
        {%- if y.arche_prop %}
        arche_prop="{{ y.arche_prop }}",
        {%- endif %}
        {%- if y.arche_prop_str_template %}
        arche_prop_str_template="{{ y.arche_prop_str_template }}",
        {%- endif %}
    )
    {%- endfor %}
    orig_data_csv = models.TextField(
        blank=True,
        null=True,
        verbose_name="The original data"
        ).set_extra(
            is_public=True
        )

    class Meta:
        {% if x.model_order == 'nan' %}
        ordering = [
            'id',
        ]
        {%- else %}
        ordering = [
            '{{ x.model_order }}',
        ]
        {%- endif %}
        verbose_name = "{{ x.model_verbose_name }}"
    {% if x.model_representation == 'nan' %}
    def __str__(self):
        return "{}".format(self.id)
    {%- else %}
    def __str__(self):
        if self.{{ x.model_representation }}:
            return "{}".format(self.{{ x.model_representation }})
        else:
            return "{}".format(self.legacy_id)
    {%- endif %}

    def field_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_listview_url(self):
        return reverse('{{ app_name }}:{{ x.model_name|lower }}_browse')
    {% if x.source_table %}
    @classmethod
    def get_source_table(self):
        return "{{ x.source_table }}"
    {% else %}
    @classmethod
    def get_source_table(self):
        return None
    {% endif %}
    {% if x.natural_primary_key %}
    @classmethod
    def get_natural_primary_key(self):
        return "{{ x.natural_primary_key }}"
    {% else %}
    @classmethod
    def get_natural_primary_key(self):
        return None
    {% endif %}
    @classmethod
    def get_createview_url(self):
        return reverse('{{ app_name }}:{{ x.model_name|lower }}_create')

    def get_absolute_url(self):
        return reverse('{{ app_name }}:{{ x.model_name|lower }}_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('{{ app_name }}:{{ x.model_name|lower }}_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('{{ app_name }}:{{ x.model_name|lower }}_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = next_in_order(self)
        if next:
            return reverse(
                '{{ app_name }}:{{ x.model_name|lower }}_detail',
                kwargs={'pk': next.id}
            )
        return False

    def get_prev(self):
        prev = prev_in_order(self)
        if prev:
            return reverse(
                '{{ app_name }}:{{ x.model_name|lower }}_detail',
                kwargs={'pk': prev.id}
            )
        return False

{% endfor %}
"""
