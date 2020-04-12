
## Near Future Climate Model
- ~100 years of time scale
- CO2 concentration = Natural constant + Human External Growth
- Given the CO2 concentrationn, calculate RF from that
- Delt*T_eq = C * RF
  - C = Cliamte Sensitivity
  - RF = ?
  - In reality, Delt\*T_eq could be a more complicated function of RF

## Radiative Forcing
- Definition
  - Measure of the amount that the Earth's energy budget is out of balance. So, it's defined after putting CO2 in the air, but before the temperature has had a chance to change.
- Other things
  - Can be measured in the boundary between the troposphere and the stratosphere
  - Many different factors contributing to forcing overlap and some factors are confounding (e.g. different GHG absorb and emit at the same infrared wavelengths of radiation) 
  - 1850 - "zero point" for radiative forcing before industrialization 
  - One factor overwhelmingly affects the uncertainty - aerosol
- Masking
  - Masked radiative forcing == reduced radiative forcing

## T_eq
  - Temperature that the planet is relaxing to given enough time
  - There's long, non-negligible time scale for how long it takes for the planet to reach T_eq.
  - T_transient -> T_eq

## About the model
- Goal: Simulate the near-term future of Earth's climate as a function of 3 uncertainties : Future CO2 admissions, C (climate senst), and cooling / masking effect from industrial aerosols.

- Time stepping calculation
  - First stage: People releasing CO_2 and generating aerosols (biz as usual)
  - Second stage: We stop both things (CO_2 persists, aerosol goes away)

- Numerical guts

  - Biz-as-usual CO2 increases exponentially
    - pCO2 (time 2) = 280 + (pCO2 (time 1)-280) * (1 + A * D_time)
      - A: Tunable growth rate parameter
      - D_time = time step
  - For each pCO2, calculate radiative forcing
    - RF from CO2 = 4 * ln ( pCO2 / 280 ) / ln (2)
      - Last factor is the # of doublings of the CO2 concentration over an initial value
  - Account for masking
    - Intensity of masking depends of rate of industrial activity
    - RF masking scaled = B * (pCO2 (year 2015) – pCO2 (year 2014))/( 1 year)
      - B : factor that you can get by fitting a RF estimate for the _present_ day. In other words, to get a masking effect of –0.75 Watts / m2, when the pCO2 rise is 2.5 ppm / year, B would have to be –0.3. Solve for it assuming present-day masking RF is -0.75
      - Reasonable if function works only for the past. But further increases in CO2 emissions can increase aerosol furthers; RF masking = max ( RF masking scaled, masking in 2015)
  - Total RF = RF from CO2 + RF masking 
  - Compute the Delt\*T_eq from the total RF 
    - Use climate sensitivity; climate_sensitivity_Watts_m2 = climate_sensitivity_2x / 4 [Watts/m2 per doubling CO2]
  - Compute the evolution of temperature by relaxing toward eq. on a time scale of 100 years
    - change in T per timestep = (T(equilibrium) – T) / t_response_time (20 years) * X years / timestep

  - The world without us; 
  - when pCO_2 hits 400, let new pCO2 values be:
    - change in CO2 per timestep = ( 340 - CO2 ) * ( 0.01 * timestep )
    - CO2 concentration is relaxing towards a higher conc. than the initial due to long-term change in ocean chemistry (acidification). CO2 invasion into the ocean is 100 years (composite of fast eq. with surface, slower with deep)
  - Compute the RF from CO2 from this 
  - Compute the T_eq from the RF from CO2
  - Compute the time-evolving temp. from this period 



