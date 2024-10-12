[Shared Components](#shared-components)
1. [Button](#button)
2. [Checkbox](#checkbox)
3. [Radio button](#radio-button)
4. [Select](#select)
5. [Form](#form)
6. [Table](#table)
7. [List](#list)
8. [Dropdown](#dropdown)
9. [Tooltip](#tooltip)
10. [Icon](#icon)
11. [Popup](#popup)
12. [Message under Breadcrumb](#message-under-breadcrumbs)
13. [Datepicker](#datepicker)
14. [Images](#image)
15. [Label](#label)
16. [Dynamic Options List](#dynamic-options-list)

[Coding Patterns and Others](#coding-patterns-and-others)
1. [Auto width columns](#auto-width-columns)
2. [Implementing popups](#implementing-popups)
3. [API calls](#api-calls)
4. [Confirm message](#confirm-message)
5. [Notifications](#notifications)
6. [The lodash library](#the-lodash-library)
7. [Communication between React and non-React code](#communication-between-react-and-non-react-code)
8. [Performance optimizations](#performance-optimizations)
9. [ESLint](#eslint)

## Shared Components

Below you will find example uses for the most common cases, but you can check the components' propTypes to see all available props.

You can find them in `app/javascript/src/shared/components`.

### Button
```
%GlgButton(text="URL Button"
           href="www.golfgenius.com")
%GlgButton(text="onClick Button"
           onClick={ () => {} })
%GlgButton(text="Small Grey Button"
           href="www.golfgenius.com"
           color="gray"
           size="small")
```

### Checkbox
```
%GlgCheckbox(name="managers"
             value="managers"
             label="Managers (uncontrolled)"
             defaultChecked={ true }
             onChange={ (val) => {} })
%GlgCheckbox(name="managers2"
             value="managers2"
             label="Managers (controlled)"
             checked={ boolVariable })
```

### Radio button
```
%GlgRadio(name="league[product]"
          value="event"
          label="Event"
          inline={ true }
          defaultChecked={ true })
```

### Select
```
const options = [
  {
    value: 'all',
    label: 'All',
  },
  {
    value: 'upcoming',
    label: 'Upcoming',
  },
]
%GlgSelect(items={ options }
           value={ this.props.value }
           onChange={ this.onChange }
           disabled={ this.props.disabled }
           defaultValue="upcoming")

%GlgSelect(name="tour"
           searchable={ true }
           items={ this.props.tours })
```

### Form
```
%GlgForm
  %GlgFormInput(label="Name")
    %FormControl(name="league[name]"
                 type="text"
                 value={ this.state.name })
  %GlgFormInput(label="Season")
     %GlgSelect(name="season"
                items={ this.props.seasons })
```

You should wrap `GlgForm` children in either a `GlgFormInput` or a `GlgFormTextInput` component. The second one is just a specialization or the first.

If the form is inside a popup, use `GlgPopupForm` instead.

### Table
```
const leagues = [
  {
    name: 'League name',
    seasonName: 'Season name',
  },
  ...
]
%GlgTable(items={ leagues }
          rowComponent={ LeagueRowComponent }
          isSortable={ true }
          onSortEnd={ (fromIndex, toIndex) => {} })
  %GlgTableCol(width="20%" dataKey="Name")
  {this.props.showSeasons && (~
    %GlgTableCol(width="10%" dataKey="Season")
  ~)}

const LeagueRowComponent = ({ isSortable, ...props }) => (~
  %GlgTableRow({ ...props } isSortable={ isSortable })
    %GlgTableCell
      { props.name }
    {props.showSeasons && (~
      %GlgTableCell
        { props.seasonName }
    ~)}
~)
```

The array of items must be objects that contain at least an `id` field. It can also be an array of ids if the `rowComponent` is a container and it fetches the `id` field.

### List
```
%GlgList(items={ this.props.categories }
         itemComponent={ CategoryComponent }
         isSortable={ true }
         onSortEnd={ this.handleCategoriesSortEnd })
```

Same as for `GlgTable`, the array of items must be objects that contain at least an `id` field.

### Dropdown
```
const dropdownOptions = [
  {
    label: 'Restore',
    onClick: () => restore(id),
  },
  {
    label: 'Go to League',
    url: leagueURL,
  },
]
%GlgDropdown(items={ dropdownOptions }
             direction="left")
```

If you want to customize the button and the menu of the dropdown component, there is `GlgCustomDropdown`.

### Tooltip
```
%GlgTooltipIcon(tooltip="Tooltip text!")

%GlgTooltip(tooltip="Tooltip with a custom element!")
  %div
    Hello
```

Customizing the tooltip

```
%GlgTooltipIcon(tooltip="Tooltip text!"
                tooltipClass="custom-tooltip")
``` 

Styling
```
.tooltip.custom-tooltip > .tooltip-inner
  max-width: 300px
```

### Icon
```
%GlgIcon(icon="carret-down")

import { Icon as FaIcon } from 'react-fa'
%FaIcon(name="pencil-square-o")
```

### Popup
```
%GlgPopup(title="New Category"
          saveButtonText="Save"
          show={ this.props.showPopup }
          onClose={ this.onClose }
          onSave={ this.onSave })
  %GlgPopupForm
    %GlgFormInput(label="Color")
      %GlgColorPicker(name="list[color]" initialColor="red")
```

More details on [implementing popups](#implementing-popups).

### Message under Breadcrumb
```
%StickToBreadcrumb
  Notice that is under the breadcrumbs.
```

### Datepicker
```
%GlgDatePicker(name="start_date"
               onChange={ this.handleDateChange })
...
handleDateChange(date) {
  // date's format is MM/DD/YYYY
}
```

### Image
```
import { Image } from 'react-bootstrap'

%Image(src={ require('home/genius/bios/zisman.jpg') }
       circle={ true })

const photoURL = require('report_center/no-image.png')
%Image(src={ photoURL })
```

### Label
```
%GlgLabel(type="success")
  Label text
```

### Dynamic Options List

This is what it looks like ([link](https://cl.ly/6a78b134b0a7)).

```
%GlgOptionsList(inputName="help_links"
                columns={ [ 'name', 'url' ] }
                defaultOptionValues={ [ { name: 'initial option', url: 'initial url 1' }, ... ] }
                placeholders={ [ 'Title', 'URL' ] })
```

## Coding Patterns and Others

### Auto width columns

With the help of [flexboxgrid](https://roylee0704.github.io/react-flexbox-grid/) we can implement columns with auto widths. Because they conflict with the old Bootstrap columns, we can only enable them on the pages where we use them. This means we need to wrap our view in a `.flexbox-context`.

```
import { Row, Col } from 'react-flexbox-grid'

%Row
  %Col(xs={true})
    Column 1
  %Col(xs={6})
    Column 2
  %Col(xs={true})
    Column 3
```

Column 2 will take up half of the width, while columns 1 and 3 will each take up a quarter of the width.

### Implementing popups

You can either

1. *[recomended]* Create a top-level component that contains all of the popups and manage its state with Redux, or
2. *[optional]* Put the popup component inside a [portal](https://reactjs.org/docs/portals.html) and manage its state from the parent component.

Code sample for 1.
```
> reducers/index.js
import popupReducerCreator from 'Shared/reducers/popup_reducer_creator'
import PopupTypes from '../popup_types'
const popupStates = popupReducerCreator(PopupTypes)

> actions/index.js
import { PopupActionTypes } from 'Shared/actions'
export { openPopup, closePopup } from 'Shared/actions'
export const ActionTypes = {
  ...PopupActionTypes,
  ...
}

> Popup component
this.onClose = props.onClose.bind(this, PopupTypes.CREATE_EVENT)
...
%GlgPopup(onClose={ this.onClose } ...)
```

If you need multiple popups stacked on each other, you don't need to worry about this. The last activated (`show={ true }`) popup will always be on top.

### API calls

You sometimes need to call an API endpoint after a UI event (e.g. button click, drag&drop). You will do this in the action creator. Using [redux-thunk](https://github.com/reduxjs/redux-thunk) we can make async action creators.

```
import { callAPI, showErrorNotification } from 'Shared/helpers'

export const updateCategory = (id, data) => (dispatch, getState) => {
  ...
  callAPI(url, 'POST', {
    format: 'json',
    list: {
      name: data.name,
      ...
    },
  })
  .then(json => {
    console.log('Received this ' + json)
  })
  .catch(() => {
    showErrorNotification('Error while updating a category!')
  })
  dispatch({
    type: ActionTypes.UPDATE_CATEGORY,
    id,
    data,
  })
}
```

### Confirm message

Instead of using the browser built-in confirm, we use a popup-based one.

```
import { onConfirm } from 'Shared/helpers'
...
onClick() {
  onConfirm('Are you sure you want to delete this category?', () => {
    this.props.deleteCategory(this.props.id)
  })
}
```

### Notifications

Put the container in the root component, then just use the helper functions.

```
import { NotificationContainer } from 'react-notifications'

%RootComponent
  ...
  %NotificationContainer

...
import { showErrorNotification, showNotification } from 'Shared/helpers'
showNotification(`Successfully created category ${ data.name }.`)
showErrorNotification(responseData.errorMessages)
```

### The lodash library
A lot of [lodash](https://lodash.com/docs/) methods are very useful in a React/Redux context.
```
import _ from 'lodash'

if (_.isEmpty({ x: 3 })) { ... }
const personCount = _.size({ 123: 'George' })
const ids = _.keys({ 123: 'George' })
const names = _.values({ 123: 'George' })

const arrayWithoutAValue = _.without([123, 2, 1, 3], 123)
const arrayWithoutLowValues = _.filter([123, 2, 1, 3], leagueId > 100)

const person = { id: 123, name: 'George', age: 26 }
const personWithoutNameField = _.omit(person, 'name')
const personWithIdAndNameFields = _.pick(person, [ 'id', 'name' ])

const clonedOjbect = _.clone(object)
const deepClonedArray = _.cloneDeep(array)

const sortedLeagues = _.sortBy(leagues, league => league.name)

const leagueText = _.capitalize('league')
```

The equivalent of this Rails code
```
object.try(:field)
```
in React is
```
import { get } from 'lodash'
get(object, 'field')
```

### Communication between React and non-React code
```
// After creating the store, expose it as a global object
window.glg.dispatch = store.dispatch

// jQuery code
$(document).on "click", ".create_new_league_from_header", (event) ->
  window.glg.dispatch
    type: 'OPEN_POPUP'
```

### Performance optimizations

You should avoid multiple renders when not necessary. To test which components do this, uncomment the code in `app/javascript/packs/application.js`, refresh the page and check the console. After you identified the components that need to be optimized, either make them pure components (`extends PureComponent`) or implement the `shouldComponentUpdate` method.

### ESLint

To make sure the code quality stays at a high level we are using [ESLint](https://eslint.org/). It is recommended that you run `./bin/webpack-dev-server` while developing so that the feedback is instantaneous and because hot reloading is awesome.

If you are just testing out something, you can *temporarily* place `/* eslint-disable */` at the top of the file.
