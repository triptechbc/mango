from django.db import models


# Create your models here.
class Filenames(models.Model):
    filename = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date')

    def __str__(self):
        return self.filename


class Data(models.Model):
    filename = models.ForeignKey(Filenames, on_delete=models.CASCADE)
    voltage = models.FloatField()
    current = models.FloatField()

    def __str__(self):
        return "Voltage: {0}, Current: {1}".format(self.voltage, self.current)


class Assignments(models.Model):
    def __str__(self):
        return self.title

    title = models.CharField(max_length=200)
    date_created = models.DateTimeField('date')
    text = models.CharField(max_length=256)
    metadata1 = models.CharField(max_length=256)
    metadata2 = models.CharField(max_length=256)


class Submissions(models.Model):
    def __str__(self):
        return self.student_name

    student_name = models.CharField(max_length=200)
    assignment = models.ForeignKey(Assignments, on_delete=models.CASCADE)
    date = models.DateTimeField('date')
    data_location = models.CharField(max_length=256)
    metadata1 = models.CharField(max_length=256)
    metadata2 = models.CharField(max_length=256)
