import logging

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.generic.edit import View
from django.forms.models import model_to_dict

from shortly_app.forms import LinkCreateForm
from shortly_app.models import Link

logger = logging.getLogger(__name__)


class HomeView(View):
    """
    A class used to represent a main page

    ...

    Attributes
    ----------
    form_class : ModelForm
       form used to create new links
    template_name : str
       the name of current template
    paginate_by : int
       number of links on one page
    default_page : int
       number default page display (default 1)

    Methods
    -------
    _create_paginator(self, user_links, page):
       Create links paginator
    """

    form_class = LinkCreateForm
    template_name = 'index.html'
    paginate_by = 5
    default_page = 1

    def get(self, request, *args, **kwargs):
        link_form = self.form_class
        page = request.GET.get('page', self.default_page)
        user_links = request.session.get('user_links', [])
        user_links_pag = self._create_paginator(user_links, page)

        context = {
            "form": link_form,
            'items': user_links_pag,
            'host': request.get_host()
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        link_form = self.form_class(request.POST)
        if link_form.is_valid():
            new_link = link_form.save(commit=False)
            if not new_link.subpart:
                new_link.subpart = Link.generate_subpart(url=new_link.url)
            new_link.save()

            logger.info('new link {}'.format(new_link))

            new_link = model_to_dict(new_link)
            if request.session.get('user_links'):
                request.session['user_links'].append(new_link)
                request.session.modified = True
            else:
                request.session['user_links'] = [new_link]

            user_links_pag = self._create_paginator(request.session['user_links'], page=self.default_page)

            context = {
                'form': self.form_class(),
                'short_url': new_link['subpart'],
                'items': user_links_pag,
                'host': request.get_host()
            }
            return render(request, self.template_name, context)

        else:
            context = {
                'form': link_form,
                'items': self._create_paginator(request.session['user_links'], page=self.default_page),
                'host': request.get_host()
            }
            return render(request, self.template_name, context)

    def _create_paginator(self, user_links, page):
        paginator = Paginator(user_links[::-1], self.paginate_by)
        if user_links:
            try:
                user_links = paginator.page(page)
            except PageNotAnInteger:
                user_links = paginator.page(self.default_page)
            except EmptyPage:
                user_links = paginator.page(paginator.num_pages)

        return user_links
