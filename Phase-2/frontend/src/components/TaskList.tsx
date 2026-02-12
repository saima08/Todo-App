/**
 * Task List Component - Display tasks with status indicators
 * Task: T031 [US2]
 * Task: T033 [US2]
 * Task: T055 [US6]
 */
"use client";

import { useState } from "react";

interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  priority: string;
  tags: string[];
  due_date?: string;
  recurring?: string;
  created_at: string;
  updated_at: string;
}

interface TaskListProps {
  tasks: Task[];
  loading?: boolean;
  onToggleComplete?: (taskId: number) => void;
  onUpdate?: (taskId: number) => void;
  onDelete?: (taskId: number) => void;
}

export default function TaskList({
  tasks,
  loading = false,
  onToggleComplete,
  onUpdate,
  onDelete,
}: TaskListProps) {
  if (loading) {
    return (
      <div className="flex justify-center py-10">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent" />
      </div>
    );
  }

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-gray-900">
          Tasks <span className="text-gray-400">({tasks.length})</span>
        </h2>
      </div>

      {tasks.length === 0 ? (
        <div className="rounded-xl border bg-white p-10 text-center shadow-sm">
          <p className="text-gray-500">
            No tasks found. Adjust filters or create a new task.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {tasks.map((task) => (
            <div
              key={task.id}
              className="group rounded-xl border bg-white p-5 shadow-sm transition hover:shadow-md"
            >
              <div className="flex gap-4">
                {/* Checkbox */}
                {onToggleComplete && (
                  <button
                    onClick={() => onToggleComplete(task.id)}
                    className="mt-1"
                    aria-label={
                      task.completed ? "Mark incomplete" : "Mark complete"
                    }
                  >
                    <div
                      className={`flex h-5 w-5 items-center justify-center rounded border-2 transition ${
                        task.completed
                          ? "border-green-600 bg-green-600"
                          : "border-gray-300 hover:border-gray-400"
                      }`}
                    >
                      {task.completed && (
                        <svg
                          className="h-3 w-3 text-white"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="3"
                        >
                          <path d="M5 13l4 4L19 7" />
                        </svg>
                      )}
                    </div>
                  </button>
                )}

                {/* Content */}
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <h3
                      className={`font-semibold ${
                        task.completed
                          ? "line-through text-gray-400"
                          : "text-gray-900"
                      }`}
                    >
                      {task.title}
                    </h3>

                    {/* Priority */}
                    <span
                      className={`rounded-full px-2 py-0.5 text-xs font-semibold ${
                        task.priority === "high"
                          ? "bg-red-100 text-red-700"
                          : task.priority === "medium"
                          ? "bg-yellow-100 text-yellow-700"
                          : "bg-green-100 text-green-700"
                      }`}
                    >
                      {task.priority.toUpperCase()}
                    </span>
                  </div>

                  {task.description && (
                    <p
                      className={`mt-1 text-sm ${
                        task.completed
                          ? "text-gray-400"
                          : "text-gray-600"
                      }`}
                    >
                      {task.description}
                    </p>
                  )}

                  {/* Tags */}
                  {task.tags.length > 0 && (
                    <div className="mt-3 flex flex-wrap gap-2">
                      {task.tags.map((tag, i) => (
                        <span
                          key={i}
                          className="rounded-full bg-blue-100 px-2 py-0.5 text-xs text-blue-800"
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Meta */}
                  <div className="mt-3 flex flex-wrap gap-4 text-xs text-gray-500">
                    {task.due_date && (
                      <span className="text-orange-600">
                        Due: {new Date(task.due_date).toLocaleString()}
                      </span>
                    )}
                    {task.recurring && task.recurring !== "none" && (
                      <span className="text-purple-600">
                        Recurring: {task.recurring}
                      </span>
                    )}
                  </div>

                  <div className="mt-2 text-xs text-gray-400">
                    Created:{" "}
                    {new Date(task.created_at).toLocaleDateString()}
                    {task.updated_at !== task.created_at && (
                      <>
                        {" "}
                        • Updated:{" "}
                        {new Date(task.updated_at).toLocaleDateString()}
                      </>
                    )}
                  </div>
                </div>

                {/* Right side */}
                <div className="flex flex-col items-end gap-3">
                  <span
                    className={`rounded-full px-3 py-1 text-xs font-semibold ${
                      task.completed
                        ? "bg-green-100 text-green-800"
                        : "bg-yellow-100 text-yellow-800"
                    }`}
                  >
                    {task.completed ? "Completed" : "Pending"}
                  </span>

                  {/* Actions */}
                  <div className="flex gap-2 opacity-0 transition group-hover:opacity-100">
                    {onUpdate && (
                      <button
                        onClick={() => onUpdate(task.id)}
                        className="rounded-md p-1 text-gray-400 hover:bg-gray-100 hover:text-blue-600"
                        aria-label="Edit"
                      >
                        ✏️
                      </button>
                    )}
                    {onDelete && (
                      <button
                        onClick={() => onDelete(task.id)}
                        className="rounded-md p-1 text-gray-400 hover:bg-red-50 hover:text-red-600"
                        aria-label="Delete"
                      >
                        🗑
                      </button>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}