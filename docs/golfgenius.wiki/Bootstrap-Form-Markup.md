```
.btsp_form_content
  %ul.btsp_ul                
    %li.form_row
      .row
        .col-sm-3.col-md-3.col-lg-3.hidden-xs
          = f.label :name 
        .col-xs-12.col-sm-9.col-md-9.col-lg-9
          .description.col-xs-12.col-sm-12.col-md-12.col-lg-12
            .bold
              = "Edit the round name"
            .clear
              The round name appears on the #{@league.product.titleize} Portal, TV Leaderboard, and reports.
          .content_fields.col-xs-12.col-sm-12.col-md-12.col-lg-12
            .col-xs-12.col-sm-6.col-md-6.col-lg-6.no-padding
              = f.text_field :name, value: @round.name, class: "form-control form-text"

```