'use client'

import { NavHeader } from '@/components/nav-header'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Checkbox } from '@/components/ui/checkbox'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog'
import { ArrowLeft, Save, Trash2 } from 'lucide-react'
import Link from 'next/link'
import { useState } from 'react'
import { useRouter } from 'next/navigation'

const categories = ['Ação', 'Aventura', 'RPG', 'Indie', 'Estratégia', 'Simulação', 'Plataforma', 'Horror']

export default function EditGamePage() {
  const router = useRouter()
  const [name, setName] = useState('The Last of Us Part II')
  const [description, setDescription] = useState('The Last of Us Part II é um jogo eletrônico de ação-aventura desenvolvido pela Naughty Dog.')
  const [price, setPrice] = useState('39.99')
  const [selectedCategories, setSelectedCategories] = useState(['Ação', 'Aventura'])

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault()
    console.log('Game saved:', { name, description, price, selectedCategories })
    router.push('/admin')
  }

  const handleDelete = () => {
    console.log('Game deleted')
    router.push('/admin')
  }

  const toggleCategory = (category: string) => {
    setSelectedCategories(prev =>
      prev.includes(category)
        ? prev.filter(c => c !== category)
        : [...prev, category]
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <NavHeader />
      
      <main className="container mx-auto px-4 py-8 max-w-3xl">
        <Link href="/admin" className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground mb-6 transition-colors">
          <ArrowLeft className="h-4 w-4 mr-1" />
          Voltar para admin
        </Link>

        <Card>
          <CardHeader>
            <CardTitle>Editar Jogo</CardTitle>
            <CardDescription>
              Atualize as informações do jogo
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSave} className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="name">Nome do Jogo</Label>
                <Input
                  id="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="description">Descrição</Label>
                <Textarea
                  id="description"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  rows={5}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="price">Preço Atual ($)</Label>
                <Input
                  id="price"
                  type="number"
                  step="0.01"
                  value={price}
                  onChange={(e) => setPrice(e.target.value)}
                  required
                />
              </div>

              <div className="space-y-3">
                <Label>Categorias</Label>
                <div className="grid grid-cols-2 gap-4">
                  {categories.map((category) => (
                    <div key={category} className="flex items-center space-x-2">
                      <Checkbox
                        id={category}
                        checked={selectedCategories.includes(category)}
                        onCheckedChange={() => toggleCategory(category)}
                      />
                      <label
                        htmlFor={category}
                        className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
                      >
                        {category}
                      </label>
                    </div>
                  ))}
                </div>
                <div className="flex flex-wrap gap-2 mt-2">
                  {selectedCategories.map((cat) => (
                    <Badge key={cat}>{cat}</Badge>
                  ))}
                </div>
              </div>

              <div className="flex gap-3 pt-4">
                <Button type="submit" className="flex-1 gap-2">
                  <Save className="h-4 w-4" />
                  Salvar Alterações
                </Button>
                
                <AlertDialog>
                  <AlertDialogTrigger asChild>
                    <Button type="button" variant="destructive" className="gap-2">
                      <Trash2 className="h-4 w-4" />
                      Excluir
                    </Button>
                  </AlertDialogTrigger>
                  <AlertDialogContent>
                    <AlertDialogHeader>
                      <AlertDialogTitle>Excluir jogo?</AlertDialogTitle>
                      <AlertDialogDescription>
                        Esta ação não pode ser desfeita. O jogo será permanentemente removido do sistema.
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>Cancelar</AlertDialogCancel>
                      <AlertDialogAction onClick={handleDelete} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
                        Excluir
                      </AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
              </div>
            </form>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
