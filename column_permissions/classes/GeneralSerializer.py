from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.apps import apps


class GeneralSerializer(serializers.ModelSerializer):
    class Meta:
        fields = []
        required_fields = None
        

    # art_parent = CustomerHyperlink(
    #     view_name="ph_products:general-detail", lookup_field='id', read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        display_fields = kwargs.pop('display_fields', fields)
        model = kwargs.pop('model', None)
        if fields == None:
            raise Exception("You should have permission to see this model")

        required_fields = kwargs.pop('required_fields', None)
        exclude_fields = kwargs.pop('exclude_fields', None)
    
        super(GeneralSerializer, self).__init__(*args, **kwargs)
        self.Meta.model = model
        if fields:
            self.Meta.fields = fields
        if required_fields:
            self.Meta.required_fields = required_fields
        if display_fields:
            self.Meta.display_fields = display_fields

        if exclude_fields:
            self.Meta.exclude_fields = exclude_fields

    def get_photo_url(self, photo):

        request = self.context.get('request')
        if photo and hasattr(photo, 'url'):
            photo_url = photo.url
            return request.build_absolute_uri(photo_url)
        else:
            return None

    def get_view_name(self, obj):
        view_name = obj._meta.app_label+":general-detail"
        return view_name

    def get_obj_api_url(self, obj):
        # try:
        view_name = self.get_view_name(obj)
        url_kwargs = {
            'pk': str(obj.id)+"," + obj._meta.app_label+","+type(obj).__name__
        }
        request = self.context.get('request')
        obj_url = reverse(view_name, kwargs=url_kwargs,
                          request=request, format=None)
        return obj_url
        # except Exception as e:
        #     return str(e.args)

    def to_representation(self, instance):
        # try:
        result = {}
        # return super().to_representation(instance)
        # representation = super().to_representation(instance)
        fields = self.Meta.display_fields
        if fields == '__all__':
            model_fields = self.Meta.model._meta.get_fields()
            fields = [field.name for field in model_fields]
        # fields.append('href')

        for field in fields:
            try:
                model_field = self.Meta.model._meta.get_field(field)
                field_value = getattr(instance, field)
            except Exception as e:
                field_value = str(e.args)
                result[field] = field_value
                continue

            model_field_type_name = type(model_field).__name__
            if model_field_type_name in ['ManyToManyField', 'ManyToOneRel', 'ManyToManyRel']:
                field_values = field_value.all()
                field_values_list = []

                for value in field_values:
                    name = ""
                    try:
                        name = value.get_name
                    except:
                        name = value.__str__()
                    elem = {'id': value.id, 'name': name}
                    photo = None
                    try:
                        photo = value.get_image
                        image = None
                        try:
                            image = self.get_photo_url(photo)
                        except:
                            pass
                        if image:
                            elem['image'] = image
                    except:
                        pass

                    href = None
                    href = self.get_obj_api_url(value)
                    if href:
                        elem['href'] = href

                    field_values_list.append(elem)
                result[field] = field_values_list

            elif model_field_type_name in ['ForeignKey', 'GenericForeignKey', 'OneToOneField', 'OneToOneRel']:
                if field_value and not isinstance(field_value,ContentType):
                    name = ""
                    try:
                        name = field_value.get_name
                    except:
                        name = field_value.__str__()
                    elem = {'id': field_value.id, 'name': name}
                    photo = None
                    try:
                        photo = field_value.get_image
                        image = None
                        try:
                            image = self.get_photo_url(photo)
                        except:
                            pass
                        if image:
                            elem['image'] = image
                    except Exception as e:
                        pass

                    href = None
                    href = self.get_obj_api_url(field_value)
                    if href:
                        elem['href'] = href

                else:
                    elem = None
                result[field] = elem

            elif model_field_type_name in ['ImageField', 'FileField']:
                result[field] = self.get_photo_url(field_value)

            elif model_field_type_name == 'UUIDField':
                if field_value:
                    result[field] = field_value.__str__()
                else:
                    result[field] = None

            elif model_field_type_name == 'DateTimeField':
                result[field] = field_value.__str__()

            elif model_field_type_name == 'PhoneNumberField':
                result[field] = str(field_value)

            else:
                result[field] = field_value
        if not (hasattr(instance, 'name')):
            name = getattr(instance, 'get_name', None)
            if name:
                result['name'] = name

        main_img = getattr(instance, 'get_image', None)
        if main_img:
            image = self.get_photo_url(main_img)
            result['main_img'] = image

        return result
        # except Exception as e:
        #     raise {'error': str(e.args)+" "+field}
