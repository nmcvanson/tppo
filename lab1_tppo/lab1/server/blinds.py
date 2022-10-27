import time

class Blinds():
    path = "../server/blinds.txt"

    @staticmethod
    def read_database(path):
        with open(path, "r") as file:
            data = file.readlines()
            file.close()
        return data

    def get_params(self, path = path):
        data = self.read_database(path)
        shift_percentage = int(data[0].split()[-1])
        luminous_flux_percentage = int(data[1].split()[-1])
        current_illumination = int(data[2].split()[-1])
        return shift_percentage, luminous_flux_percentage, current_illumination

    def __init__(self):
        self.shift_percentage, self.luminous_flux_percentage, self.current_illumination = self.get_params()

    def get_shift_percentage(self):
        return self.shift_percentage
    
    def get_luminous_flux_percentage(self):
        return self.luminous_flux_percentage

    def get_current_illumination(self):
        return self.current_illumination

    def set_shift(self, new_shift, path = path):
        """
        Установить проценты сдвига полотна

        """
        data_ = self.read_database(path)
        shift = data_[0].split()
        shift[-1] = str(new_shift)
        data_[0] = ' '.join(shift)+'\n'

        with open(path, 'w') as file:
            file.writelines(data_)
            file.close()
        self.shift_percentage = str(new_shift)

    def set_luminous_flux(self, new_luminous_flux, path = path):
        """
        Установить проценты сдвига полотна

        """
        data_ = self.read_database(path)
        luminous_flux = data_[1].split()
        luminous_flux[-1] = str(new_luminous_flux)
        data_[1] = ' '.join(luminous_flux)+'\n'

        with open(path, 'w') as file:
            file.writelines(data_)
            file.close()
        self.luminous_flux_percentage = str(new_luminous_flux)






