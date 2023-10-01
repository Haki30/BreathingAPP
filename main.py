from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from random import randint
import serial


class SensorDataLayout(BoxLayout):
    def __init__(self, close_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.oxygen_level_label = Label(text='Niveli i Oksigjenit: ')
        self.respiratory_rate_label = Label(text='Ritmi i Frymëmarrjes: ')
        self.close_button = Button(text='Mbylle', background_color=(0.8, 0.8, 0.8, 1))
        self.close_button.bind(on_press=self.close_window)
        self.add_widget(self.oxygen_level_label)
        self.add_widget(self.respiratory_rate_label)
        self.add_widget(self.close_button)
        self.close_callback = close_callback

    def update_sensor_data(self, oxygen_level, respiratory_rate):
        self.oxygen_level_label.text = f'Niveli i Oksigjenit: {oxygen_level}'
        self.respiratory_rate_label.text = f'Ritmi i Frymëmarrjes: {respiratory_rate}'

    def close_window(self, instance):
        self.close_callback()


class BreathingApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        sensor_data_button = Button(text='Të dhënat e Sensorëve', background_color=(1, 0, 0, 1))
        sensor_data_button.bind(on_press=self.show_sensor_data)
        compare_data_button = Button(text='Krahaso të Dhënat', background_color=(0, 0, 1, 1))
        compare_data_button.bind(on_press=self.show_compare_data)
        breathing_exercises_button = Button(text='Ushtrime për frymëmarrje', background_color=(0, 1, 0, 1))
        breathing_exercises_button.bind(on_press=self.show_breathing_exercises)

        layout.add_widget(sensor_data_button)
        layout.add_widget(compare_data_button)
        layout.add_widget(breathing_exercises_button)

        contact_us_label = Label(text='Contact Us: +355-688080888', halign='right', valign='middle', size_hint_y=None,
                                 height=40)
        layout.add_widget(contact_us_label)

        return layout

    def show_sensor_data(self, instance):
        oxygen_level, respiratory_rate = self.generate_sensor_data()
        sensor_data_layout = SensorDataLayout(close_callback=self.close_sensor_data_window)
        sensor_data_layout.update_sensor_data(oxygen_level, respiratory_rate)
        scrollable_label = ScrollView()
        scrollable_label.add_widget(sensor_data_layout)
        self.sensor_data_popup = Popup(title='Të dhënat e Sensorëve', content=scrollable_label,
                                       size_hint=(None, None), size=(1000, 600))
        self.sensor_data_popup.open()

    def close_sensor_data_window(self):
        self.sensor_data_popup.dismiss()

    def ard_info(self):
        arduino_port = 'COM5'
        arduino_baudrate = 9600

        ser = serial.Serial(arduino_port, arduino_baudrate)

        line = ser.readline().decode().strip()
        print(f'Oxygen Level: {line}')

        ser.close()

        return line

    def generate_sensor_data(self):
        oxygen_level = randint(90, 100)
        respiratory_rate = randint(12, 20)
        return oxygen_level, respiratory_rate

    def show_compare_data(self, instance):
        oxygen_level, respiratory_rate = self.generate_sensor_data()
        compare_result = self.compare_data_with_normal_range(oxygen_level, respiratory_rate)
        layout = BoxLayout(orientation='vertical', padding=(10, 10), spacing=10)
        label = Label(text=compare_result)
        close_button = Button(text='Mbylle', on_press=self.close_compare_data_window)
        layout.add_widget(label)
        layout.add_widget(close_button)
        self.compare_data_popup = Popup(title='Krahaso të Dhënat', content=layout,
                                        size_hint=(None, None), size=(1000, 600))
        self.compare_data_popup.open()

    def close_compare_data_window(self, instance):
        self.compare_data_popup.dismiss()

    def compare_data_with_normal_range(self, oxygen_level, respiratory_rate):
        compare_result = ''
        if 95 <= oxygen_level <= 100:
            compare_result += 'Niveli Normal i Oksigjenit\n'
        else:
            compare_result += f'Niveli Anormal i Oksigjenit: {oxygen_level}\n'

        if 12 <= respiratory_rate <= 16:
            compare_result += 'Ritmi Normal i Frymëmarrjes\n'
        else:
            compare_result += f'Ritmi Anormal i Frymëmarrjes: {respiratory_rate}\n'

        return compare_result

    def show_breathing_exercises(self, instance):
        layout = BoxLayout(orientation='vertical', padding=(50, 100), spacing=10)
        deep_breathing_button = Button(text='Frymëmarrje e Thellë', on_press=self.show_deep_breathing_instructions)
        box_breathing_button = Button(text='Frymëmarrje e Balancuar', on_press=self.show_box_breathing_instructions)
        close_button = Button(text='Mbylle', on_press=self.close_breathing_exercises_window)
        layout.add_widget(deep_breathing_button)
        layout.add_widget(box_breathing_button)
        layout.add_widget(close_button)
        self.breathing_exercises_popup = Popup(title='Ushtrime për frymëmarrje', content=layout,
                                               size_hint=(None, None), size=(1200, 600))
        self.breathing_exercises_popup.open()

    def close_breathing_exercises_window(self, instance):
        self.breathing_exercises_popup.dismiss()

    def show_deep_breathing_instructions(self, instance):
        layout = BoxLayout(orientation='vertical', padding=(50, 100), spacing=10)

        scrollview = ScrollView(do_scroll_x=False, do_scroll_y=True)

        label = Label(
            text='''Udhëzime për ushtrimin Frymëmarrje e Thellë:
    1. Qëndroni rehat. Mund të uleheni në shtrat ose në dysheme \n me një jastëk nën kokë dhe gjunjë. \n Ose mund të uleni në një karrige me shpatullat,\n kokën dhe qafën që mbështeten në prapavijën e karriges.
    2. Frymëzoni nëpërmjet hundës tuaj. \n Lëreni barkun të mbushet me ajër.
    3. Frymëzoni nëpërmjet hundës tuaj.
    4. Vendosni një dorë në bark. \n Vendosni dorën tjetër në qafë.
    5. Gjatë frymëzimit, ndjeni si barku juaj ngrit. \n Gjatë zmadhimit, ndjeni si barku juaj zbret.
    6. Frymëzoni thellë për rreth 10 sekonda, pastaj lëshoni ajrin ngadalë.
    7. Përsëriteni këtë mënyrë frymëmarrjeje për 5-10 minuta.
    8. Relaksohuni dhe ndjeni frymëmarrjen tuaj të qetë dhe të rregullt.''',
            valign='top',
            size_hint=(None, None),
            size=(1200, 850),
            text_size=(None, None),
            markup=True,
        )
        label.bind(size=label.setter("text_size"))

        scrollview.add_widget(label)

        layout.add_widget(scrollview)

        back_button = Button(text="Kthehu Mbrapa", size_hint=(None, None), size=(300, 50),
                             on_press=self.close_deep_breathing_exercises_window)

        layout.add_widget(back_button)

        self.deep_breathing_exercises_popup = Popup(title='Frymemarrje e thelle', content=layout,
                                                    size_hint=(None, None), size=(1500, 1000))
        self.deep_breathing_exercises_popup.open()

    def close_deep_breathing_exercises_window(self, instance):
        self.deep_breathing_exercises_popup.dismiss()

    def show_box_breathing_instructions(self, instance):
        scrollview = ScrollView(do_scroll_x=False, do_scroll_y=True)

        instruction_label = Label(
            text='''Udhëzime për Ushtrime për frymëmarrjen e balancuar:
1. Qëndroni rehat në një vend të qetë.
2. Merrni fryme thellë dhe ngadalë për 4 sekonda. 
3. Mbani frymën tuaj për 4 sekonda. 
4. Lëshoni frymën tuaj ngadalë për 4 sekonda. 
5. Mbani pa frymë për 4 sekonda. 
6. Përsëritni këtë mënyrë frymëmarrjeje për 5-10 minuta.
7. Relaksohuni dhe ndjeni frymëmarrjen tuaj të qetë dhe të rregullt
''',
            valign='top',
            size_hint=(None, None),
            size=(1200, 850),
            text_size=(None, None),
            markup=True,
        )
        instruction_label.bind(size=instruction_label.setter("text_size"))
        scrollview.add_widget(instruction_label)
        popup = Popup(title='Frymëmarrje e balancuar', content=scrollview,
                      size_hint=(None, None), size=(1200, 850))
        popup.open()


if __name__ == '__main__':
    BreathingApp().run()
