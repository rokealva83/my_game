# -*- coding: utf-8 -*-

import math
import random
from django.shortcuts import render
from my_game.models import Galaxy, System, Planet


def star_generation(request):
    if request.method == "POST" and request.POST.get('add_button') is not None:
        last_galaxy = Galaxy.objects.last()
        if last_galaxy:
            galaxy = Galaxy(
                x=last_galaxy.x,
                y=last_galaxy.y,
                z=last_galaxy.z + 12000,
            )
            galaxy.save()
        else:
            galaxy = Galaxy(
                x=0,
                y=0,
                z=0,
            )
            galaxy.save()

        system_id = 0
        r = 5
        angle = 45
        star = int(request.POST.get('star', None))
        iteration = 0
        gal = [[0, 0, 0, 0, 0, 0, 0, 0]]
        x2 = y2 = z2 = size2 = star_type = 0
        galaxy.save()
        while (system_id <= star):
            # координаты систем
            mark = 1
            while mark > 0:
                mark = 0
                sys = []
                sys.append(int(system_id))

                # генерация координат систем
                Zm = random.randint(0, 20)
                x = 2 * (r + Zm) * math.cos(angle)
                Zm = random.randint(0, 20)
                y = 1.5 * (r + Zm) * math.sin(angle)
                z = random.randint(-30, 30)
                system_size = random.randint(4000, 9000)
                system_size = float(system_size)
                system_size = system_size / 1000
                sys.append(int(x))
                sys.append(int(y))
                sys.append(int(z))
                sys.append(system_size)

                # класификация звезд
                k = random.random()
                if k > 0.05:
                    star_type = 0
                else:
                    star_type = 1
                sys.append(star_type)

                # тест на правильность координат
                for i in range(iteration):
                    j = 2
                    x2 = gal[i][j]
                    y2 = gal[i][j + 1]
                    z2 = gal[i][j + 2]
                    size2 = gal[i][j + 3]
                ligth = math.sqrt((x - x2) ** 2 + (y - y2) ** 2 + (z - z2) ** 2)
                size = system_size + size2
                if 2 * size > ligth:
                    mark = mark + 1

            # расчет радиусов орбит планет
            radius_star = round(system_size / 3 * 1000, 2)
            radius = (system_size * 1000 - (radius_star)) / 12

            system = System(
                galaxy=galaxy,
                x=x * 1000,
                y=y * 1000,
                z=z * 1000,
                system_type=star_type,
                system_size=system_size,
                star_size=radius_star
            )
            system.save()

            # количество планет в системе
            k = random.random()
            if 0.01 > k:
                n = 0
            else:
                if 0.01 <= k <= 0.1:
                    n = random.randint(1, 4)
                else:
                    if 0.1 < k < 0.3:
                        n = random.randint(10, 12)
                    else:
                        n = random.randint(5, 9)

            plans = [[0, 0, 0, 0, 0]]
            # проверка на правильность
            for ii in range(n):
                q = ii
                mark1 = 1
                while mark1 > 0:
                    planet_id = random.randint(1, 12)
                    mark1 = 0
                    for jj in range(q + 1):
                        w = int(plans[jj][0])
                        if planet_id == w:
                            mark1 = mark1 + 1

                # генерация координат планет и радиусов орбиты
                plan = []
                plan.append(planet_id)
                angle_orbit = random.randint(1, 360)
                dev = random.randint(-25, 25)
                orb_radius = radius_star + planet_id * radius
                system_x = orb_radius * math.cos(angle_orbit)
                system_y = orb_radius * math.sin(angle_orbit)
                system_z = random.randint(-15, 15)
                global_x = x * 1000 + system_x
                global_y = y * 1000 + system_y
                global_z = z * 1000 + system_z
                plan.append(int(system_x))
                plan.append(int(system_y))
                plan.append(system_z)

                # генерация планет, их размера и класса
                planet_type = 0
                planet_size = radius / random.randint(8, 12)
                planet_type = random.randint(1, 5)
                plan.append(planet_type)
                plan.append(round(planet_size, 3))

                planet_area = 4 * math.pi * planet_size
                planet_work_area = planet_area * 0.65 * 100
                plan.append(round(planet_work_area))


                # скорость и направление смещения планет
                planet_displacement_vector = round(random.randint(0, 1))
                if planet_displacement_vector == 0:
                    planet_displacement_vector = -1
                planet_offset_angle = round(360.000000 / random.randint(200, 1000), 8)
                plan.append(planet_offset_angle)
                plan.append(planet_displacement_vector)

                planet = Planet(
                    system=system,
                    global_x=global_x,
                    global_y=global_y,
                    global_z=global_z,
                    system_x=system_x,
                    system_y=system_y,
                    system_z=system_z,
                    planet_num=planet_id,
                    planet_type=planet_type,
                    planet_size=planet_size,
                    orb_radius=orb_radius,
                    area_planet=planet_area,
                    work_area_planet=planet_work_area,
                    planet_displacement_vector=planet_displacement_vector,
                    planet_offset_angle=planet_offset_angle
                )
                planet.save()
                plans.append(plan)
                plans.sort()
            gal.append(sys)
            system_id = system_id + 1
            iteration = iteration + 1
            r = r + 1
            a = a + 15
    return render(request, "admin/generation.html", {})
