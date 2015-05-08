# -*- coding: utf-8 -*-


import random
from django.shortcuts import render
from my_game.models import System, Asteroid_field


def asteroid_generation(request):
    if request.method == "POST" and request.POST.get('add_button') is not None:

        asteroid = int(request.POST.get('asteroid', None))
        for i in range(asteroid):
            system = System.objects.filter().order_by('x').first()
            x_min = system.x - 10
            system = System.objects.filter().order_by('x').last()
            x_max = system.x + 10
            system = System.objects.filter().order_by('y').first()
            y_min = system.y - 10
            system = System.objects.filter().order_by('y').last()
            y_max = system.y + 10
            x = round(random.uniform(x_min, x_max), 3)
            y = round(random.uniform(y_min, y_max), 3)
            z = round(random.uniform(-30, 30), 3)

            k = random.random()
            if 0.07 > k:
                size = random.randint(3000000, 5000000)
            else:
                if 0.07 <= k <= 0.2:
                    size = random.randint(1000000, 3000000)
                else:
                    if 0.2 < k < 0.8:
                        size = random.randint(500000, 1000000)
                    else:
                        size = random.randint(100000, 500000)

            k = random.random()
            if 0.02 > k:
                artifact = 5
            elif 0.02 <= k <= 0.1:
                artifact = 4
            elif 0.1 < k <= 0.2:
                artifact = 3
            elif 0.2 < k <= 0.4:
                artifact = 2
            elif 0.4 < k <= 0.7:
                artifact = 1
            else:
                artifact = 0

            k = random.random()
            if 0.05 > k:
                ore = round(random.uniform(0.8, 0.95), 3)
            elif 0.05 <= k <= 0.35:
                ore = round(random.uniform(0.799, 0.8), 3)
            else:
                ore = round(random.uniform(0.6, 0.799), 3)

            mineral_koef = round(random.uniform(0.07, 0.2), 3) * ore
            resource_koef = ore - mineral_koef

            koef_res_1 = round(round(random.uniform(0.2, 0.3), 3) * resource_koef, 3)
            koef_res_2 = round(round(random.uniform(0.2, 0.3), 3) * resource_koef, 3)
            koef_res_3 = round(round(random.uniform(0.2, 0.3), 3) * resource_koef, 3)
            koef_res_4 = round(resource_koef - (koef_res_1 + koef_res_2 + koef_res_3), 3)
            koef_min_1 = round(round(random.uniform(0.2, 0.3), 3) * mineral_koef, 3)
            koef_min_2 = round(round(random.uniform(0.2, 0.3), 3) * mineral_koef, 3)
            koef_min_3 = round(round(random.uniform(0.2, 0.3), 3) * mineral_koef, 3)
            koef_min_4 = round(mineral_koef - (koef_min_1 + koef_min_2 + koef_min_3), 3)

            asteroid_test = Asteroid_field.objects.filter(x = x, y = y, z = z).first()

            if asteroid_test:
                size = size = asteroid_test.size
                koef_res_1 = asteroid_test.koef_res_1
                koef_res_2 = asteroid_test.koef_res_2
                koef_res_3 = asteroid_test.koef_res_3
                koef_res_4 = asteroid_test.koef_res_4
                koef_min_1 = asteroid_test.koef_min_1
                koef_min_2 = asteroid_test.koef_min_2
                koef_min_3 = asteroid_test.koef_min_3
                koef_min_4 = asteroid_test.koef_min_4

                asteroid = Asteroid_field(
                    x = x,
                    y = y,
                    z = z,
                    size = size,
                    koef_res_1 = koef_res_1,
                    koef_res_2 = koef_res_2,
                    koef_res_3 = koef_res_3,
                    koef_res_4 = koef_res_4,
                    koef_min_1 = koef_min_1,
                    koef_min_2 = koef_min_2,
                    koef_min_3 = koef_min_3,
                    koef_min_4 = koef_min_4,
                    artifact = artifact
                )
                asteroid.save()
            else:
                asteroid = Asteroid_field(
                    x = x,
                    y = y,
                    z = z,
                    size = size,
                    koef_res_1 = koef_res_1,
                    koef_res_2 = koef_res_2,
                    koef_res_3 = koef_res_3,
                    koef_res_4 = koef_res_4,
                    koef_min_1 = koef_min_1,
                    koef_min_2 = koef_min_2,
                    koef_min_3 = koef_min_3,
                    koef_min_4 = koef_min_4,
                    artifact = artifact
                )
                asteroid.save()


        message = 'Поля сгенерированы'
        output = {'message': message}

        return render(request, "admin/generation.html", output)
