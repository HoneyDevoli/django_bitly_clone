from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.generic.edit import View
from django.forms.models import model_to_dict

from shortly_app.forms import LinkCreateForm
from shortly_app.models import Link


class HomeView(View):
    form_class = LinkCreateForm
    template_name = 'index.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        link_form = self.form_class
        page = request.GET.get('page', 1)
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

            print(model_to_dict(new_link))
            new_link = model_to_dict(new_link)
            if request.session.get('user_links'):
                request.session['user_links'].append(new_link)
                request.session.modified = True
            else:
                request.session['user_links'] = [new_link]

            user_links_pag = self._create_paginator(request.session['user_links'], page=1)

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
                'items': self._create_paginator(request.session['user_links'], page=1),
                'host': request.get_host()
            }
            return render(request, self.template_name, context)

    def _create_paginator(self, user_links, page):
        paginator = Paginator(user_links, self.paginate_by)
        if user_links:
            try:
                user_links = paginator.page(page)
            except PageNotAnInteger:
                user_links = paginator.page(1)
            except EmptyPage:
                user_links = paginator.page(paginator.num_pages)

        return user_links
