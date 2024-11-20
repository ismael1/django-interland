# class Perfil(models.Model):
#     usuario = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.CharField(max_length=255, blank=True)
#     web = models.URLField(blank=True)

#     # Python 3
#     def __str__(self): 
#         return self.usuario.username

# @receiver(post_save, sender=User)
# def crear_usuario_perfil(sender, instance, created, **kwargs):
#     if created:
#         Perfil.objects.create(usuario=instance)

# @receiver(post_save, sender=User)
# def guardar_usuario_perfil(sender, instance, **kwargs):
#     instance.perfil.save()