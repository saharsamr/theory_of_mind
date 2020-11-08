class Interaction:

    @staticmethod
    def instrutions_allowed_keys(image_index, num_of_images):

        if image_index == 0 and num_of_images == 1:
            return ['space']
        elif image_index == 0:
            return ['left']
        elif image_index == num_of_images -1:
            return ['space', 'right']
        else:
            return ['right', 'left']
