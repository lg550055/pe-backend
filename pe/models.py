from django.db import models


class Estimate(models.Model):
  symbol = models.CharField(max_length=8, unique=True)
  industry = models.CharField(max_length=32, blank=True, null=True)
  sector = models.CharField(max_length=32, blank=True, null=True)
  num_analysts = models.PositiveSmallIntegerField()
  fwd_eps = models.DecimalField(max_digits=7, decimal_places=2)
  fwd2_eps = models.DecimalField(max_digits=7, decimal_places=2)
  fwd_rev = models.DecimalField(max_digits=9, decimal_places=2)
  fwd2_rev = models.DecimalField(max_digits=9, decimal_places=2)
  fwd_rev_g = models.DecimalField(max_digits=5, decimal_places=4)
  fwd2_rev_g = models.DecimalField(max_digits=5, decimal_places=4)
  shrs_out = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  # TTM
  trail_date = models.CharField(max_length=10, blank=True, null=True)
  trail_rev = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  trail_ebitda = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  trail_cfo = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  trail_capex = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  # most recent fy
  date1 = models.CharField(max_length=10, blank=True, null=True)
  ndebt1 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  rev1 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  ebitda1 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  cfo1 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  capex1 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  # 2 fy ago
  date2 = models.CharField(max_length=10, blank=True, null=True)
  ndebt2 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  rev2 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  ebitda2 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  cfo2 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  capex2 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  # 3 fy ago
  date3 = models.CharField(max_length=10, blank=True, null=True)
  ndebt3 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  rev3 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  ebitda3 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  cfo3 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  capex3 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  # 4 fy ago
  date4 = models.CharField(max_length=10, blank=True, null=True)
  ndebt4 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  rev4 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  ebitda4 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  cfo4 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  capex4 = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  notes = models.CharField(max_length=256, blank=True, null=True)
  created = models.DateField(auto_now_add=True)
  modified = models.DateField(auto_now=True)

  def __str__(self) -> str:
    return self.symbol
