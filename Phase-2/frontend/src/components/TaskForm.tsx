/**
 * Task Creation Form Component
 * Task: T025 [US1], T054 [US6]
 * UI Enhanced – Functionality unchanged
 */
"use client";

import { useState } from "react";

interface TaskFormProps {
  onSubmit: (data: {
    title: string;
    description?: string;
    priority?: "high" | "medium" | "low";
    tags?: string[];
    due_date?: string;
    recurring?: string;
  }) => Promise<void>;
  loading?: boolean;
}

export default function TaskForm({ onSubmit, loading = false }: TaskFormProps) {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    priority: "medium" as "high" | "medium" | "low",
    tagInput: "",
    tags: [] as string[],
    due_date: "",
    recurring: "none",
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = "Title is required";
    } else if (formData.title.length > 200) {
      newErrors.title = "Title must be 200 characters or less";
    }

    if (formData.description && formData.description.length > 1000) {
      newErrors.description = "Description must be 1000 characters or less";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    try {
      const submitData: any = {
        title: formData.title.trim(),
        description: formData.description.trim() || undefined,
        priority: formData.priority,
        tags: formData.tags,
      };

      if (formData.due_date) {
        submitData.due_date = new Date(formData.due_date).toISOString();
      }

      if (formData.recurring && formData.recurring !== "none") {
        submitData.recurring = formData.recurring;
      }

      await onSubmit(submitData);

      setFormData({
        title: "",
        description: "",
        priority: "medium",
        tagInput: "",
        tags: [],
        due_date: "",
        recurring: "none",
      });
      setErrors({});
    } catch {
      setErrors({ submit: "Failed to create task" });
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-xl border bg-white p-6 shadow-sm space-y-6"
    >
      <h2 className="text-xl font-semibold text-gray-900">
        Create New Task
      </h2>

      {errors.submit && (
        <div className="rounded-lg bg-red-50 p-3 text-sm text-red-700">
          {errors.submit}
        </div>
      )}

      {/* Title */}
      <div>
        <label className="text-sm font-medium text-gray-700">
          Title <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          value={formData.title}
          onChange={(e) =>
            setFormData({ ...formData, title: e.target.value })
          }
          maxLength={200}
          disabled={loading}
          placeholder="Task title"
          className="mt-1 w-full rounded-lg border px-4 py-2 text-sm focus:border-blue-500 focus:ring-blue-500"
        />
        {errors.title && (
          <p className="mt-1 text-xs text-red-600">{errors.title}</p>
        )}
        <p className="mt-1 text-xs text-gray-400">
          {formData.title.length}/200
        </p>
      </div>

      {/* Description */}
      <div>
        <label className="text-sm font-medium text-gray-700">
          Description
        </label>
        <textarea
          rows={3}
          value={formData.description}
          onChange={(e) =>
            setFormData({ ...formData, description: e.target.value })
          }
          maxLength={1000}
          disabled={loading}
          placeholder="Optional task details"
          className="mt-1 w-full rounded-lg border px-4 py-2 text-sm focus:border-blue-500 focus:ring-blue-500"
        />
        <p className="mt-1 text-xs text-gray-400">
          {formData.description.length}/1000
        </p>
      </div>

      {/* Priority + Due Date */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="text-sm font-medium text-gray-700">
            Priority
          </label>
          <select
            value={formData.priority}
            onChange={(e) =>
              setFormData({
                ...formData,
                priority: e.target.value as "high" | "medium" | "low",
              })
            }
            disabled={loading}
            className="mt-1 w-full rounded-lg border px-4 py-2 text-sm"
          >
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>

        <div>
          <label className="text-sm font-medium text-gray-700">
            Due Date
          </label>
          <input
            type="datetime-local"
            value={formData.due_date}
            onChange={(e) =>
              setFormData({ ...formData, due_date: e.target.value })
            }
            disabled={loading}
            className="mt-1 w-full rounded-lg border px-4 py-2 text-sm"
          />
        </div>
      </div>

      {/* Tags */}
      <div>
        <label className="text-sm font-medium text-gray-700">
          Tags
        </label>
        <div className="mt-1 flex gap-2">
          <input
            type="text"
            value={formData.tagInput}
            onChange={(e) =>
              setFormData({ ...formData, tagInput: e.target.value })
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                const tag = formData.tagInput.trim();
                if (tag && !formData.tags.includes(tag)) {
                  setFormData({
                    ...formData,
                    tags: [...formData.tags, tag],
                    tagInput: "",
                  });
                }
              }
            }}
            placeholder="Add tag & press Enter"
            disabled={loading}
            className="flex-1 rounded-lg border px-4 py-2 text-sm"
          />

          <button
            type="button"
            disabled={loading}
            onClick={() => {
              const tag = formData.tagInput.trim();
              if (tag && !formData.tags.includes(tag)) {
                setFormData({
                  ...formData,
                  tags: [...formData.tags, tag],
                  tagInput: "",
                });
              }
            }}
            className="rounded-lg border bg-gray-50 px-4 py-2 text-sm font-medium hover:bg-gray-100"
          >
            Add
          </button>
        </div>

        {formData.tags.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-2">
            {formData.tags.map((tag, i) => (
              <span
                key={i}
                className="flex items-center gap-1 rounded-full bg-blue-100 px-3 py-1 text-xs text-blue-800"
              >
                #{tag}
                <button
                  type="button"
                  onClick={() =>
                    setFormData({
                      ...formData,
                      tags: formData.tags.filter((_, index) => index !== i),
                    })
                  }
                  className="hover:text-blue-600"
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Recurring */}
      <div>
        <label className="text-sm font-medium text-gray-700">
          Recurring
        </label>
        <select
          value={formData.recurring}
          onChange={(e) =>
            setFormData({ ...formData, recurring: e.target.value })
          }
          disabled={loading}
          className="mt-1 w-full rounded-lg border px-4 py-2 text-sm"
        >
          <option value="none">None</option>
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
          <option value="yearly">Yearly</option>
        </select>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full rounded-lg bg-blue-600 py-2.5 text-sm font-semibold text-white hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Creating..." : "Create Task"}
      </button>
    </form>
  );
}