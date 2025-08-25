from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def grade_calculator():
    result = None
    error = None

    if request.method == "POST":
        try:
            # Inputs
            absences = float(request.form.get("absences", 0))
            prelim_exam = float(request.form.get("prelim_exam", 0))
            quizzes = float(request.form.get("quizzes", 0))
            requirements = float(request.form.get("requirements", 0))
            recitation = float(request.form.get("recitation", 0))

            # Validate inputs
            if absences < 0 or absences > 4 or not all(0 <= g <= 100 for g in [prelim_exam, quizzes, requirements, recitation]):
                error = "Invalid input: Grades must be 0-100, absences 0-4"
            elif absences >= 4:
                result = {"status": "FAILED due to excessive absences"}
            else:
                # Attendance
                attendance = max(0, 100 - absences*10)

                # Class Standing
                class_standing = 0.4*quizzes + 0.3*requirements + 0.3*recitation

                # Prelim Grade
                prelim_grade = 0.6*prelim_exam + 0.1*attendance + 0.3*class_standing

                # Function for required Midterm + Final average
                def required_avg(target_overall):
                    # Overall = 0.2*Prelim + 0.3*Midterm + 0.5*Final
                    # Assume Midterm = Final = X
                    return (target_overall - 0.2*prelim_grade)/0.8

                # Prelim pass threshold
                final_status = ""
                if prelim_grade < 75:
                    final_status = "FAILED (Prelim below 75)"
                elif prelim_grade >= 90:
                    final_status = "Congratulations! You made it to the Dean's List!. You PASSED!"
                else:
                    final_status = "You Passed!"

                result = {
                    
                    "prelim_grade": round(prelim_grade, 2),
                    "pass_needed": round(required_avg(75), 2),
                    "deans_needed": round(required_avg(90), 2),
                    "final_status": final_status
                }

        except ValueError:
            error = "Please enter valid numbers."

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=False)
