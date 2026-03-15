clc;
clear;
close all;

% ✅ Load CSV
data = readtable('attendance.csv');

disp("Attendance Data:");
disp(data);

% ✅ Total Attendance Records
total_records = height(data);
fprintf('Total Attendance Records: %d\n', total_records);

% ✅ Unique Students
students = unique(data.student);
num_students = length(students);
fprintf('Unique Students: %d\n', num_students);

% ✅ Attendance Count per Student
attendance_count = groupcounts(data, "student");

disp("Attendance Count per Student:");
disp(attendance_count);

% ✅ Bar Graph
figure;
bar(attendance_count.GroupCount);
set(gca, 'XTickLabel', attendance_count.student);
xlabel('Students');
ylabel('Attendance Count');
title('Attendance per Student');
grid on;

% ✅ Pie Chart
figure;
pie(attendance_count.GroupCount, attendance_count.student);
title('Attendance Distribution');

% ✅ Percentage Calculation
percentages = (attendance_count.GroupCount / total_records) * 100;

disp("Attendance Percentage:");
for i = 1:num_students
    fprintf('%s → %.2f %%\n', students{i}, percentages(i));
end
saveas(figure(1), 'bar_chart.png');
saveas(figure(2), 'pie_chart.png');
