from django.db import models


class AddDressPiece(models.Model):
    dress_piece = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.dress_piece


class AddColor(models.Model):
    color_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.color_name


class AddDressFabric(models.Model):
    fabric_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.fabric_name


class AddDressDesign(models.Model):
    design_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.design_name


class AddFragranceType(models.Model):
    fragrance_type_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.fragrance_type_name


class AddScentType(models.Model):
    scent_type_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.scent_type_name


class AddFoundationType(models.Model):
    foundation_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.foundation_name


class AddHighlighterType(models.Model):
    highlighter_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.highlighter_name


class AddShoeType(models.Model):
    shoe_type_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.shoe_type_name


class AddBagType(models.Model):
    bag_type_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.bag_type_name


class Suit(models.Model):
    dress = models.ForeignKey(AddDressPiece, on_delete=models.CASCADE)
    color = models.ForeignKey(AddColor, on_delete=models.CASCADE)
    fabric = models.ForeignKey(AddDressFabric, on_delete=models.CASCADE)
    design = models.ForeignKey(AddDressDesign, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images', blank=True)
    link = models.TextField()

    def __str__(self) -> str:
        return self.link


class Perfume(models.Model):
    perfume_type = models.ForeignKey(AddFragranceType, on_delete=models.CASCADE)
    scent = models.ForeignKey(AddScentType, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images/perfumes/', blank=True)
    link = models.TextField()

    def __str__(self) -> str:
        return self.link


class Highlighter(models.Model):
    highlighter_type = models.ForeignKey(AddHighlighterType, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images/highlighters/', blank=True)
    link = models.TextField()

    def __str__(self) -> str:
        return self.link


class Shoe(models.Model):
    shoe_type = models.ForeignKey(AddShoeType, on_delete=models.CASCADE)
    color = models.ForeignKey(AddColor, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images/shoes/', blank=True)
    link = models.TextField()

    def __str__(self) -> str:
        return self.link


class Bag(models.Model):
    bag_type = models.ForeignKey(AddBagType, on_delete=models.CASCADE)
    color = models.ForeignKey(AddColor, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images/bags/', blank=True)
    link = models.TextField()

    def __str__(self) -> str:
        return self.link


class AddGreeting(models.Model):
    query = models.TextField('Query in Comma Separated Values: ')
    response = models.TextField()

    def __str__(self) -> str:
        return self.query


class AddFarewell(models.Model):
    query = models.TextField('Query in Comma Separated Values: ')
    response = models.TextField()

    def __str__(self) -> str:
        return self.query