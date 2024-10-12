* Golfers may or may not have genders in the scope of a league / event.
* For golfers without a gender, we want first try to use the default gender specified in the league / event profile.
* If that is blank, we try to use the majority gender - the gender used by most golfers in the league / event.

Code example:


```    
    # set data depeding if data is setup by gender on round level
    @gender_metadata_answers ||= {}
    member_answer = gender_metadata_answers[@member.id]
    
    if member_answer.blank?
      member_answer = @engine.league.default_gender
      if member_answer.blank?
        member_answer = @engine.league.get_most_used_gender
      end
    end
```