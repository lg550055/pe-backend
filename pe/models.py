from django.db import models


class Estimate(models.Model):
  symbol = models.CharField(max_length=8, unique=True)
  num_analysts = models.PositiveSmallIntegerField()
  fwd_eps = models.DecimalField(max_digits=5, decimal_places=2)
  fwd2_eps = models.DecimalField(max_digits=5, decimal_places=2)
  fwd_rev = models.DecimalField(max_digits=9, decimal_places=2)
  fwd2_rev = models.DecimalField(max_digits=9, decimal_places=2)
  fwd_rev_g = models.DecimalField(max_digits=5, decimal_places=4)
  fwd2_rev_g = models.DecimalField(max_digits=5, decimal_places=4)
  created = models.DateField(auto_now_add=True)
  modified = models.DateField(auto_now=True)

  def __str__(self) -> str:
    return self.symbol
