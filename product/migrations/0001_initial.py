# Generated by Django 4.2.2 on 2023-07-08 22:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.TextField()),
                ('number', models.IntegerField()),
                ('zipCode', models.BigIntegerField()),
                ('neighborhood', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.TextField()),
                ('middleName', models.TextField()),
                ('lastName', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Taste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taste_name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Combo',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.product')),
            ],
            bases=('product.product',),
        ),
        migrations.CreateModel(
            name='Drink',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.product')),
                ('volume', models.FloatField()),
            ],
            bases=('product.product',),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('cpf', models.BigIntegerField(primary_key=True, serialize=False)),
                ('telephoneNumber', models.TextField()),
                ('email', models.TextField()),
                ('password', models.TextField()),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.address')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.name')),
            ],
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.product')),
                ('tastes', models.ManyToManyField(to='product.taste')),
            ],
            bases=('product.product',),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.order')),
                ('combo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.combo')),
                ('drink', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.drink')),
                ('pizza', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.pizza')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('drink', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.drink')),
                ('pizza', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.pizza')),
            ],
        ),
        migrations.AddField(
            model_name='combo',
            name='item',
            field=models.ManyToManyField(to='product.item'),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.cart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('combo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.combo')),
                ('drink', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.drink')),
                ('pizza', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.pizza')),
            ],
        ),
    ]
