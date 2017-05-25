# stylesheet rules


Command for compile: **sass --watch main.scss:../css/style.css**

### main file:
 * style.scss
 
### tools files:
 * _variables.scss

### partials files:
 * _header.scss
 * _footer.scss
 * _restaurantprofile.scss
 * _userprofile.scss
***

# references:

#### Sass mixin @media
```css
.block__restaurant__info {
  @include bp(480px,1024px) {
    color: black;
  }
}
```
#### Css compiled

```css
.block__restaurant__info {
  @include bp(480px,1024px) {
    color: black;
  }
}
```

#### Sass mixin clearfix
```css
.session__ofert {
@include clearfix;
}
```
#### Css compiled

```css
.session__ofert {
  *zoom: 1;
  &:before,
  &:after {
    display: table;
    content: "";
    line-height: 0;
  }
    &:after {
    clear: both;
  }
}
```

######	Enjoy!
