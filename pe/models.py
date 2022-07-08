from django.db import models


class Estimate(models.Model):
  symbol = models.CharField(max_length=8, unique=True)
  industry = models.CharField(max_length=32, blank=True)
  sector = models.CharField(max_length=32, blank=True)
  num_analysts = models.PositiveSmallIntegerField()
  fwd_eps = models.DecimalField(max_digits=7, decimal_places=2)
  fwd2_eps = models.DecimalField(max_digits=7, decimal_places=2)
  fwd_rev = models.DecimalField(max_digits=9, decimal_places=2)
  fwd2_rev = models.DecimalField(max_digits=9, decimal_places=2)
  fwd_rev_g = models.DecimalField(max_digits=5, decimal_places=4)
  fwd2_rev_g = models.DecimalField(max_digits=5, decimal_places=4)
  shrs_out = models.DecimalField(max_digits=9, decimal_places=2)
  trail_rev = models.DecimalField(max_digits=9, decimal_places=2)
  trail_ebitda = models.DecimalField(max_digits=9, decimal_places=2)
  trail_cfo = models.DecimalField(max_digits=9, decimal_places=2)
  trail_capex = models.DecimalField(max_digits=9, decimal_places=2)
  p1_date = models.CharField(max_length=10, blank=True)
  p1_ndebt = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
  p1_rev = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
  p1_ebitda = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
  p1_cfo = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
  p1_capex = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
  p2_date = models.CharField(max_length=10, blank=True)
  p2_ndebt = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
  p2_rev = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
  p2_ebitda = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
  p2_cfo = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
  p2_capex = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
  p3_date = models.CharField(max_length=10, blank=True)
  p3_ndebt = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
  p3_rev = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
  p3_ebitda = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
  p3_cfo = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
  p3_capex = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
  p4_date = models.CharField(max_length=10, blank=True)
  p4_ndebt = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
  p4_rev = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
  p4_ebitda = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
  p4_cfo = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
  p4_capex = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
  notes = models.CharField(max_length=256, blank=True)
  created = models.DateField(auto_now_add=True)
  modified = models.DateField(auto_now=True)

  def __str__(self) -> str:
    return self.symbol
