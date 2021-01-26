# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:29:06 2020

@author: Hagai
"""


# קטניס אוורדין הלכה לאיבוד באיזו זירה מעצבנת, ועכשיו היא מחפשת את הסניף הקרוב של אבו־חסן למנה משולשת ראויה.

# צורת הזירה היא משולש שקודקודיו (0, 0), (2, 2) ו־(4, 0).
# קטניס מתחילה מאחד הקודקודים ומחליטה על הצעד הבא שלה כך:
# היא בוחרת אקראית באחד מקודקודי הזירה.
# היא הולכת מהמקום שבו היא נמצאת את מחצית הדרך עד לקודקוד שבחרה.
# היא מסמנת על המפה את הנקודה שהגיעה אליה.
# כתבו פונקציה בשם plot_walks, שמקבלת כפרמטר את מספר הצעדים של קטניס.
# הפונקציה תצייר מפת נקודות בגודל 4 על 4, . וכל נקודה בה מציינת מקום שקטניס סימנה במפה שלה.
# השתמשו במנועי חיפוש כדי לקרוא על פעולות קסם שיכולות לעזור לכם, ועל מודולים לשרטוט גרפים.
# שימו לב שנקודות יכולות להיות ממוקמות על x ו־y עשרוניים.
import random
import matplotlib.pyplot as plt


def get_half_way_point(self, destination):
        half_way_x = (self.x + destination[0]) / 2.0
        half_way_y = (self.y + destination[1]) / 2.0
        return (half_way_x, half_way_y)


class Point:
    def __init__(self):
        CORNERS = [(0, 0), (4, 0), (2, 2)]
        self.x, self.y = random.choice(CORNERS)
        print("A new instance of Class Point has just been made.")
    def __str__(self):
        return f"({self.x}, {self.y})"


    def plot_walks(self, num_of_steps):
        CORNERS = [(0, 0), (4, 0), (2, 2)]

        plot_sequence_x = []
        plot_sequence_y = []
        for step in range(0, num_of_steps):
            destination = random.choice(CORNERS)
            print(f'current place: {(self.x,self.y)}')
            print(f"destination: {destination}")
            half_way_point = get_half_way_point(self, destination)
            print(f'half_way_point: {half_way_point}')
            plot_sequence_x.append(half_way_point[0])
            plot_sequence_y.append(half_way_point[1])
            self.x, self.y = half_way_point

        plt.plot(plot_sequence_x, plot_sequence_y, 'mo')
        plt.axis([0, 4, 0, 4])
        plt.show()
        return


p1 = Point()
print(p1)
p1.plot_walks(10000)
# help(plt.plot)

            