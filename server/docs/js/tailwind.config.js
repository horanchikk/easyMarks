tailwind.config = {
  theme: {
    extend: {
      colors: {
            'back': '#080f11',
            'fore': '#49c491',
            'code-back': '#acacac',
            'back-light': '#7ac499',
            'fore-light': '#57c4ba',
          }
    },
    screens: {
      'mobile': {'max': '640px'},
      'tablet': {'min': '641px', 'max': '1280px'},
      'desktop': {'min': '1281px'}
    }
  }
}