# Generated by Django 2.1.3 on 2018-11-27 06:22

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.CharField(help_text='事業者法人番号', max_length=256, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='事業者名称', max_length=256)),
                ('url', models.URLField(help_text='事業者URL')),
                ('timezone', models.CharField(help_text='タイムゾーン', max_length=32)),
                ('lang', models.CharField(blank=True, help_text='言語', max_length=8, null=True)),
                ('phone', models.CharField(blank=True, help_text='電話番号', max_length=16, null=True)),
                ('fare_url', models.URLField(blank=True, help_text='オンライン購入URL', null=True)),
                ('email', models.EmailField(blank=True, help_text='事業者Eメール', max_length=254, null=True)),
            ],
            options={
                'verbose_name_plural': 'agencies',
            },
        ),
        migrations.CreateModel(
            name='AgencyJP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('official_name', models.CharField(blank=True, help_text='事業者正式名称', max_length=256, null=True)),
                ('zip_number', models.CharField(blank=True, help_text='事業者郵便番号', max_length=256, null=True)),
                ('address', models.CharField(blank=True, help_text='事業者住所', max_length=256, null=True)),
                ('president_pos', models.CharField(blank=True, help_text='代表者肩書', max_length=256, null=True)),
                ('president_name', models.CharField(blank=True, help_text='代表者氏名', max_length=256, null=True)),
                ('agency', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='agency', to='jpbusformat.Agency')),
            ],
            options={
                'verbose_name_plural': 'agencies_jp',
            },
        ),
        migrations.CreateModel(
            name='FareAttribute',
            fields=[
                ('id', models.CharField(help_text='運賃ID', max_length=256, primary_key=True, serialize=False)),
                ('price', models.IntegerField(help_text='運賃')),
                ('currency_type', models.CharField(help_text='通貨', max_length=3)),
                ('payment_method', models.IntegerField(choices=[(0, '後払い'), (1, '前払い')], help_text='支払いタイミング')),
                ('transfers', models.IntegerField(choices=[(0, '不可'), (1, '1度だけ可'), (2, '2度だけ可')], help_text='乗換')),
                ('transfer_duration', models.IntegerField(blank=True, help_text='乗換有効秒数', null=True)),
                ('agency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fare_attributes', to='jpbusformat.Agency')),
            ],
        ),
        migrations.CreateModel(
            name='FareRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FeedInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed_publisher_name', models.CharField(help_text='提供組織名', max_length=256)),
                ('feed_publisher_url', models.URLField(help_text='提供組織URL')),
                ('feed_lang', models.CharField(help_text='提供言語', max_length=2)),
                ('feed_start_date', models.DateField(blank=True, help_text='提供開始日', null=True)),
                ('feed_end_date', models.DateField(blank=True, help_text='提供終了日', null=True)),
                ('feed_version', models.CharField(blank=True, help_text='バージョン', max_length=256, null=True)),
            ],
            options={
                'verbose_name_plural': 'feed_info',
            },
        ),
        migrations.CreateModel(
            name='Frequency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(help_text='開始時刻')),
                ('end_time', models.TimeField(help_text='終了時刻')),
                ('headway_secs', models.IntegerField(help_text='運行間隔')),
                ('exact_times', models.IntegerField(blank=True, choices=[(0, '不正確'), (1, '正確')], help_text='案内精度', null=True)),
            ],
            options={
                'verbose_name_plural': 'frequencies',
            },
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.CharField(help_text='営業所ID', max_length=256, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='営業所名', max_length=256)),
                ('url', models.URLField(blank=True, help_text='営業所URL', null=True)),
                ('phone', models.CharField(blank=True, help_text='営業所電話番号', max_length=16, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.CharField(help_text='経路ID', max_length=256, primary_key=True, serialize=False)),
                ('short_name', models.CharField(help_text='経路略称', max_length=256)),
                ('long_name', models.CharField(help_text='経路名', max_length=256)),
                ('desc', models.CharField(blank=True, help_text='経路情報', max_length=256, null=True)),
                ('type', models.IntegerField(choices=[(0, 'Tram'), (1, 'Subway'), (2, 'Rail'), (3, 'Bus'), (4, 'Ferry'), (5, 'Cable Car'), (6, 'Gondola'), (7, 'Funicular')], help_text='経路情報')),
                ('url', models.URLField(blank=True, help_text='経路URL', null=True)),
                ('color', models.CharField(blank=True, help_text='経路色', max_length=6, null=True)),
                ('text_color', models.CharField(blank=True, help_text='経路文字色', max_length=6, null=True)),
                ('sort_order', models.IntegerField(blank=True, help_text='表示順序', null=True)),
                ('parent_route_id', models.CharField(blank=True, help_text='親路線ID', max_length=256, null=True)),
                ('agency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='routes', to='jpbusformat.Agency')),
            ],
            options={
                'verbose_name_plural': 'routes',
            },
        ),
        migrations.CreateModel(
            name='RouteJP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_date', models.DateField(blank=True, help_text='ダイヤ改正日', null=True)),
                ('origin_stop', models.CharField(blank=True, help_text='起点', max_length=256, null=True)),
                ('via_stop', models.CharField(blank=True, help_text='経由地', max_length=256, null=True)),
                ('destination_stop', models.CharField(blank=True, help_text='終点', max_length=256, null=True)),
                ('route', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='route', to='jpbusformat.Route')),
            ],
            options={
                'verbose_name_plural': 'routes_jp',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.CharField(help_text='運行日ID', max_length=256, primary_key=True, serialize=False)),
                ('monday', models.BooleanField(help_text='月曜日の運行')),
                ('tuesday', models.BooleanField(help_text='火曜日の運行')),
                ('wednesday', models.BooleanField(help_text='水曜日の運行')),
                ('thursday', models.BooleanField(help_text='木曜日の運行')),
                ('friday', models.BooleanField(help_text='金曜日の運行')),
                ('saturday', models.BooleanField(help_text='土曜日の運行')),
                ('sunday', models.BooleanField(help_text='日曜日の運行')),
                ('start_date', models.DateField(help_text='サービス開始日')),
                ('end_date', models.DateField(help_text='サービス終了日')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(help_text='日付')),
                ('exception_type', models.IntegerField(choices=[(1, '適用'), (2, '非適用')], help_text='運行区分')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_dates', to='jpbusformat.Service')),
            ],
        ),
        migrations.CreateModel(
            name='Shape',
            fields=[
                ('id', models.CharField(help_text='描画ID', max_length=256, primary_key=True, serialize=False)),
                ('line', django.contrib.gis.db.models.fields.LineStringField(help_text='バス路線形状', srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('id', models.CharField(help_text='停留所・標柱ID', max_length=256, primary_key=True, serialize=False)),
                ('code', models.CharField(blank=True, help_text='停留所・標柱番号', max_length=256, null=True)),
                ('name', models.CharField(help_text='停留所・標柱名称', max_length=256)),
                ('desc', models.CharField(blank=True, help_text='停留所・標柱付加情報', max_length=256, null=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(help_text='座標', srid=4326)),
                ('url', models.URLField(blank=True, help_text='停留所・標柱URL', null=True)),
                ('location_type', models.IntegerField(blank=True, choices=[(0, '標柱'), (1, '停留所')], help_text='停留所・標柱区分', null=True)),
                ('timezone', models.CharField(blank=True, help_text='タイムゾーン', max_length=32, null=True)),
                ('wheelchair_boarding', models.IntegerField(blank=True, choices=[(0, '不明'), (1, '利用可'), (2, '利用不可')], help_text='車椅子情報', null=True)),
                ('parent_station', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stops', to='jpbusformat.Stop')),
            ],
        ),
        migrations.CreateModel(
            name='StopTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_time', models.TimeField(help_text='到着時刻')),
                ('departure_time', models.TimeField(help_text='出発時刻')),
                ('sequence', models.IntegerField(help_text='通過順序')),
                ('headsign', models.CharField(blank=True, help_text='停留所行先', max_length=256, null=True)),
                ('pickup_type', models.IntegerField(blank=True, choices=[(0, '通常の乗車地'), (1, '乗車不可能'), (2, '交通機関へ要予約'), (3, '運転手へ要連絡')], help_text='乗車区分', null=True)),
                ('drop_off_type', models.IntegerField(blank=True, choices=[(0, '通常の降車地'), (1, '降車不可能'), (2, '交通機関へ要予約'), (3, '運転手へ要連絡')], help_text='降車区分', null=True)),
                ('shape_dist_traveled', models.FloatField(blank=True, help_text='通算距離', null=True)),
                ('timepoint', models.IntegerField(blank=True, choices=[(0, '曖昧な時刻'), (1, '正確な時刻')], help_text='発着時間精度', null=True)),
                ('stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stop_times', to='jpbusformat.Stop')),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transfer_type', models.IntegerField(choices=[(0, '推奨乗継地点'), (1, '時間考慮済み乗継地点'), (2, '乗継時間指定'), (3, '乗継不可能')], help_text='乗継タイプ')),
                ('min_transfer_time', models.IntegerField(blank=True, help_text='乗継時間', null=True)),
                ('from_stop', models.ForeignKey(help_text='乗継元標柱', on_delete=django.db.models.deletion.CASCADE, related_name='from_stops', to='jpbusformat.Stop')),
                ('to_stop', models.ForeignKey(help_text='乗継先標柱', on_delete=django.db.models.deletion.CASCADE, related_name='to_stops', to='jpbusformat.Stop')),
            ],
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.CharField(help_text='翻訳元日本語', max_length=256, primary_key=True, serialize=False)),
                ('lang', models.CharField(help_text='言語', max_length=8)),
                ('translation', models.CharField(help_text='翻訳先言語', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.CharField(help_text='便ID', max_length=256, primary_key=True, serialize=False)),
                ('headsign', models.CharField(blank=True, help_text='便行先', max_length=256, null=True)),
                ('short_name', models.CharField(blank=True, help_text='便名称', max_length=256, null=True)),
                ('direction_id', models.IntegerField(blank=True, choices=[(0, '復路'), (1, '往路')], help_text='上下区分', null=True)),
                ('block_id', models.CharField(blank=True, help_text='便結合区分', max_length=256, null=True)),
                ('wheelchair_accessible', models.IntegerField(blank=True, choices=[(0, '不明'), (1, '利用可'), (2, '利用不可')], help_text='車いす利用区分', null=True)),
                ('bikes_allowed', models.IntegerField(blank=True, choices=[(0, '不明'), (1, '利用可'), (2, '利用不可')], help_text='自転車持込区分', null=True)),
                ('desc', models.CharField(blank=True, help_text='便情報', max_length=256, null=True)),
                ('desc_symbol', models.CharField(blank=True, help_text='便記号', max_length=16, null=True)),
                ('office', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trips', to='jpbusformat.Office')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='jpbusformat.Route')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trips', to='jpbusformat.Service')),
                ('shape', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trips', to='jpbusformat.Shape')),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.CharField(help_text='運賃エリアID', max_length=256, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='stoptime',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stop_times', to='jpbusformat.Trip'),
        ),
        migrations.AddField(
            model_name='stop',
            name='zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stops', to='jpbusformat.Zone'),
        ),
        migrations.AddField(
            model_name='frequency',
            name='trip',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='trip', to='jpbusformat.Trip'),
        ),
        migrations.AddField(
            model_name='farerule',
            name='contains',
            field=models.ForeignKey(blank=True, help_text='通過ゾーン', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contains_fare_rules', to='jpbusformat.Zone'),
        ),
        migrations.AddField(
            model_name='farerule',
            name='destination',
            field=models.ForeignKey(blank=True, help_text='降車地ゾーン', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='destination_fare_rules', to='jpbusformat.Zone'),
        ),
        migrations.AddField(
            model_name='farerule',
            name='fare',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fare_rules', to='jpbusformat.FareAttribute'),
        ),
        migrations.AddField(
            model_name='farerule',
            name='origin',
            field=models.ForeignKey(blank=True, help_text='乗車地ゾーン', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='origin_fare_rules', to='jpbusformat.Zone'),
        ),
        migrations.AddField(
            model_name='farerule',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fare_rules', to='jpbusformat.Route'),
        ),
    ]
