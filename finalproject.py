from pptx import Presentation
prsname=raw_input("Enter Prestation name to modify: ")
prs=Presentation(prsname)
#numslides=len(prs.slides) # produces number of slides in deck
first_slide=prs.slides[0]

print(first_slide.has_notes_slide)
#slide.has_notes_slide #checks to see if slide has notes slide

notes_slide=first_slide.notes_slide

#notes_slide=slide.notes_slide : acceses nots slide
text_frame=notes_slide.notes_text_frame
text_frame.text="this is slide 1 in the notes section"

newprs=prsname.split('.') #removes pptx fromname
new=newprs[0]
prs.save(new+' with notes.pptx') #adds withnotes.pptx to name